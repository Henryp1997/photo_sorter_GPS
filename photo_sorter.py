from pprint import pprint
from PIL import Image
import piexif
import os
import glob

codec = 'ISO-8859-1'

# bounding box for Cambridge
cambs_dict = {
    'folder_name': 'Cambridge',
    'lat_min': 52.0481, # royston
    'lat_max': 52.3995, # ely
    'long_min': -0.2651, # st neots
    'long_max': 0.7113 # bury st edmunds
}

# bounding box for Manchester
mcr_dict = {
    'folder_name': 'Manchester',
    'lat_min': 53.2587, # macclesfield
    'lat_max': 53.7486, # blackburn
    'long_min': -2.5197, # leigh
    'long_max': -1.9489 # glossop
}

# bounding box for London 
ldn_dict = {
    'folder_name': 'London',
    'lat_min': 51.1091, # crawley
    'lat_max': 51.7678, # harlow
    'long_min': -0.6157, # windsor
    'long_max': 0.3708 # gravesend
}

# bounding box for Leeds
leeds_dict = {
    'folder_name': 'Leeds',
    'lat_min': 53.6833, # wakefield
    'lat_max': 53.8999, # harewood
    'long_min': -1.7564, # bradford
    'long_max': -1.3321 # micklefield
}

# bounding box for Nottingham
notts_dict = {
    'folder_name': 'Nottingham',
    'lat_min': 52.8291, # east leake
    'lat_max': 53.0376, # calverton
    'long_min': -1.2800, # trowell
    'long_max': -0.9561 # bingham
}

def exif_to_tag(exif_dict):
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict

def get_latlong_as_decimal(data):
    vals = [i[0]/i[1] for i in data]
    return vals[0] + vals[1]/60 + vals[2]/3600 # deg, mins, secs

def find_image_location(lat, long):
    for dict in [cambs_dict, mcr_dict, ldn_dict, leeds_dict, notts_dict]:
        # check latitude
        if dict['lat_min'] < lat < dict['lat_max']:
            # check longitude
            if dict['long_min'] < long < dict['long_max']:
                return dict['folder_name']

def main():
    here = f"{os.path.dirname(os.path.realpath(__file__))}"

    for filename in glob.glob(f"{here}/input_photos/*"):
        # open image
        img = Image.open(filename)

        # get EXIF data from image, specifically GPS data
        try:
            exif_dict = piexif.load(img.info.get('exif'))
            gps_dict = exif_dict['GPS']
        except:
            # there was an error parsing the EXIF dictionary
            # there's possibly missing data
            continue
        
        # calculate latitude and longitude from degrees, mins, secs
        # and convert longitude if west of 0 degrees
        lat_index = 2
        long_index = 4
        long_direction_index = 3
        lat = get_latlong_as_decimal(gps_dict[lat_index])
        long = get_latlong_as_decimal(gps_dict[long_index])
        if gps_dict[long_direction_index].decode() == 'W':
            long = -1 * long

        # locate image given defined bounding boxes
        correct_folder = find_image_location(lat, long)
        print(f"{filename}: {correct_folder}")

if __name__ == '__main__':
   main()
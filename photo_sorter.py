import os
import glob
import shutil
from PIL import Image
import piexif
import pandas as pd

codec = 'ISO-8859-1'
here = f"{os.path.dirname(os.path.realpath(__file__))}"

def exif_to_tag(exif_dict):
    """ no longer used as it produces an AttributeError on some photos """
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

def get_exif_data(img):
    try:
        exif_dict = piexif.load(img.info.get('exif'))
        gps_dict = exif_dict['GPS']
    except:
        # there was an error parsing the EXIF dictionary
        # there's possibly missing data
        return None
    
    return gps_dict

def get_latlong_as_decimal(data):
    vals = [i[0]/i[1] for i in data]
    return vals[0] + vals[1]/60 + vals[2]/3600 # deg, mins, secs

def find_image_location(lat, long):
    df = pd.read_csv(f'{here}/regions.csv')
    for i, _ in enumerate(df):
        # check latitude
        if df['lat_min'][i] < lat < df['lat_max'][i]:
            # check longitude
            if df['long_min'][i] < long < df['long_max'][i]:
                return df['folder_name'][i]

def copy_file_to_correct_folder(filename, folder):
    shortened_name = filename.split("input_photos\\")[1]
    shutil.copy(filename, f'{here}/{folder}/{shortened_name}')

def main():
    for filename in glob.glob(f"{here}/input_photos/*"):
        # open image
        img = Image.open(filename)

        # get EXIF data from image, specifically GPS data
        gps_dict = get_exif_data(img)
        if gps_dict is None:
            # no GPS data exists in file EXIF
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
        folder = find_image_location(lat, long)

        # make folder if it doesn't exist already
        if not os.path.exists(f'{here}/{folder}'):
            os.mkdir(folder)

        # copy file to folder
        copy_file_to_correct_folder(filename, folder)

if __name__ == '__main__':
   main()
# photo_sorter_GPS
Sort photos given their GPS EXIF data - place them in user defined folders. User must figure out a bounding box for their desired location

## How it works
There is a bounding box defined for each region. For example the GPS bounding box for Manchester has been defined as:
```python
# bounding box for Manchester
mcr_dict = {
    'folder_name': 'Manchester',
    'lat_min': 53.2587, # macclesfield
    'lat_max': 53.7486, # blackburn
    'long_min': -2.5197, # leigh
    'long_max': -1.9489 # glossop
}
```
using surrounding towns as the left, right, top and bottom edges of the box. Note that negative longitudes mean West of the 0° line in Greenwich. If the photo contains GPS EXIF data and if the calculated latitude and longitude lie within this bounding box, the photo is sorted in the 'Manchester' folder. The downside to this method is that if you want to sort photos into a different city, you have to manually define the bounding box - this isn't too much effort, however. 

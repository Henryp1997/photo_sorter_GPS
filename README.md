# Photo sorter by GPS region
Sort photos given their GPS EXIF data - place them in user defined folders. User must figure out a bounding box for their desired location

![image](https://github.com/user-attachments/assets/035acc4e-6cc2-41b8-a5f3-9cf24e1badb5)


## To use
1. Firstly, place all your photos into the `input_photos` directory which is in the same location as the python script
3. Figure out the bounding box for your chosen region. This is just four towns or villages North, South, West and East of the centre of your region. Take these four sets of coordinates and input them into the `regions.csv` file as defined below:
    - Town west of chosen region: find the longitude and enter it into the 'long_min' column
    - Town east of chosen region: find the longitude and enter it into the 'long_max' column
    - Town south of chosen region: find the latitude and enter it into the 'lat_min' column
    - Town north of chosen region: find the latitude and enter it into the 'lat_max' column
2. Run the script: `python3 photo_sorter.py` and the photos will be sorted into folders. The folders will be created if they don't already exist

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

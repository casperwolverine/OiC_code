import pandas as pd
from exploration_estimation_two_objects import aggregated_info, get_info
import os
import cv2

p = 0.6   #Set here the p-cutoff
offset = 3 # Specify the offset (the number of pixels around the object still counting as exploratory behavior)
inter = 7500 #The table with results will also specify the total exploration time up until this frame number
base_directory = "P:\4180000.35\2019-0024-004\NOR\Videos\Round 1" # Specify the directory the videos and DLC file can be found
DLC_name = "DLC_resnet50_NOR 2019-0024-004 Round 1Feb3shuffle1_330000" # Specify the name of the DLC file (without the animal number)
results_directory = "P:\4180000.35\2019-0024-004\NOR\Videos\Round 1\results" # Specify the directory the results must be stored, this directory doesn't have to exist
video_format = 'mp4' # Specify the video format 
make_video = True # Specify if a video must be made

results = pd.DataFrame(
    columns=['animal', 'object1', 'object2', 'inter_object1', 'inter_object2', 'l_average'])

animal_list= [28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 33, 33, 34, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38, 39, 39, 39, 40, 40, 41, 41, 42, 42, 43, 43, 44, 44, 44, 
              45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 51, 51, 51, 51, 52, 52, 53, 53, 54, 54, 55, 55, 56, 56, 57, 57, 58, 58, 59, 59, 60, 60, 60, 61, 61, 
              62, 62, 63, 63, 64, 64, 65, 65, 65, 66, 67, 67]

for (root, dirs, file) in os.walk(base_directory):
    for f in file:
        if video_format in f:
            animal_ID = f.split('.')
            animal_list.append (animal_ID[0])

if not os.path.exists(results_directory):
    os.makedirs(results_directory)

for animal in animal_list:
    animal = str(animal)

    df = pd.read_csv(base_directory+'/'+animal+DLC_name+'.csv', skiprows=2)

    coords_object1 = pd.read_csv(base_directory+'/'       
        +animal+'-bulb.csv')
    coords_object2 = pd.read_csv(base_directory+'/'                   
        +animal+'-jar.csv')

    video = base_directory+'/'+animal+'.'+video_format 
    video_fps = cv2.VideoCapture(video)
    fps = video_fps.get(cv2.CAP_PROP_FPS)

    outpath = results_directory+'/' 

    df = get_info(animal, p, offset, df, fps, coords_object1,
                  coords_object2, video, outpath, make_video) 
    results = aggregated_info(df, fps, results, animal, inter)

results.to_csv(results_directory+'/'+'_results.csv',
  index=False) 


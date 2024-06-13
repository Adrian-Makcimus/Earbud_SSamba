"""
Author: Adrian Florea
Date: 06/10/2024
"""

import os
import csv

import json
import re

import soundfile as sf
#import librosa
import random
from scipy.signal import resample


# Function to create JSON entries for each data entry
def create_json_entry(file_path, label):
    lamba_path  = '/files1/earbud_classification/audio_mamba/data'
    adjusted_path = os.path.join(lamba_path, file_path)
    return {
        "wav": adjusted_path,
        "labels": label
    }



def convert_wav_to_flac(wav_file_path, flac_file_path, wav_file_name):
    # Load the .wav file

    data, samplerate = sf.read(wav_file_path)


    # Resample the data to 16000 Hz (if it's not already at that sample rate)
    #if samplerate != 16000:
    #    data_resampled = librosa.resample(data.T, 16000).T

    if samplerate != 16000:
        new_num_samples = int(len(data)*16000/samplerate)

        data_resampled = resample(data,new_num_samples)
    # Write the resampled data to FLAC format

    save_path = os.path.join(flac_file_path,wav_file_name[:len(wav_file_name)-4] + '.flac')
    print('flac made: ', save_path)

    #sf.write(save_path, data_resampled, 16000, format='flac')

    

def resample_each(file_path, lookup, save_path, read_dir, train_data):

    with open(file_path, 'r') as file:

        for line in file: 
            # Change later so that it searches for the type of murmur
            input = line.strip()
            if input.startswith('#'):
                break

            words = input.split()
            if len(words) == 3: #ID, number of locs, fs
                
                id = words[0]
                #nlocs = words[1]
                #fs = words[2]
                #murmur_type = lookup[id]


                #if id in train_data:
                #    out_path = os.path.join(save_path,'train')
                #else: 
                #    out_path = os.path.join(save_path,'test')


            
            elif len(words) == 4 : # PV 49989_PV.hea 49989_PV.wav 49989_PV.tsv
                wav_file = words[2]
                read_file = os.path.join(read_dir,wav_file)

                if wav_file[:len(wav_file)-4] in train_data:
                    out_path = os.path.join(save_path,'train')
                else: 
                    out_path = os.path.join(save_path,'test')

                convert_wav_to_flac(wav_file_path=read_file, flac_file_path=out_path, wav_file_name=wav_file)



# Function to extract data from the txt file
def extract_data(txt_file_path):
    unique_values = set()  # Set to store unique values
    subj_murmur = {}
    

            

    return list(unique_values), subj_murmur


# Get all label types 
#Change
target_dir = '/home/icsl/Documents/adrian/earbud/raw/labels/labels.txt' #raw, lowpass, filtered
unique_labels, subj_murmur_lookup = extract_data(target_dir) #Todo, fix function

# Add all types of murmur 
murmur_lists = {}
for subject_id, murmur_type in subj_murmur_lookup.items():
    if murmur_type not in murmur_lists:
        murmur_lists[murmur_type] = []
    murmur_lists[murmur_type].append(subject_id)

train_data = []
test_data = []

#shuffle into train and test
for murmur_type, subject_list in murmur_lists.items():
    random.shuffle(subject_list)
    split_point = int(len(subject_list) * 0.8)
    train_data.extend(subject_list[:split_point])
    test_data.extend(subject_list[split_point:])


# Make json files for each 
#Change
read_dir = '/home/icsl/Documents/adrian/earbud/raw' #raw, filtered, lowpass

# make csv for label types 
csv_output = '/home/icsl/Documents/adrian/classification/audio_mamba/earbud/class_labels_indices.csv'
with open(csv_output , 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['index', 'mid','display_name'])

    for index , murmur_type in enumerate(unique_labels, start =1):
        csv_writer.writerow([index, murmur_type, murmur_type])


#where are the flac files going?
#Change
flac_file_path = '/home/icsl/Documents/adrian/classification/audio_mamba/earbud/wavs' #wavs, filt, lp 


# Loop through each file in the folder
for filename in os.listdir(read_dir):
    if filename.endswith('.txt'):
        #only open .txt files 
        file_path = os.path.join(read_dir,filename)

        resample_each(file_path=file_path, lookup = subj_murmur_lookup, save_path=flac_file_path, read_dir= read_dir, train_data = train_data)


train_json_entries = []
for subject_id in train_data:
    file_path = os.path.join('/train',f"{subject_id}.flac")
    check_path = os.path.join(flac_file_path,'train', f"{subject_id}.flac")

    if os.path.exists(check_path):
        print('good')
        train_json_entries.append(create_json_entry(file_path=file_path, label=subj_murmur_lookup[subject_id]))
    else:
        print(f"File path does not exist: {check_path}")

# Collect JSON entries for test data
test_json_entries = []
for subject_id in test_data:
    file_path = os.path.join(flac_file_path,'/eval', f"{subject_id}.flac")
    check_path = os.path.join(flac_file_path,'eval', f"{subject_id}.flac")
    if os.path.exists(check_path):
        print('good')

        test_json_entries.append(create_json_entry(file_path=file_path, label=subj_murmur_lookup[subject_id]))
    else:
        print(f"File path does not exist: {check_path}")

#Change
train_json_output_path = '/home/icsl/Documents/adrian/classification/audio_mamba/earbud/wavs/train/a.json'
test_json_output_path = '/home/icsl/Documents/adrian/classification/audio_mamba/eabud/wavs/eval/a.json'

#train_json_output_path = '/home/icsl/Documents/adrian/classification/trash/train/a.json'
#test_json_output_path = '/home/icsl/Documents/adrian/classification/trash/test/a.json'

# Write the training data JSON entries to a file
with open(train_json_output_path, 'w') as train_json_file:
    json.dump(train_json_entries, train_json_file, indent=4)

# Write the test data JSON entries to a file
with open(test_json_output_path, 'w') as test_json_file:
   json.dump(test_json_entries, test_json_file, indent=4)
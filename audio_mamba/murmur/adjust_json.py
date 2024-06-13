import json

# Define the new directory path
new_directory_path = "/audio_mamba/data/train/"
input_json = '/audio_mamba/data/train/a.json'
output_json = '/audio_mamba/data/train/circor_train.json'

new_directory_path_ev = "/audio_mamba/data/eval/"
input_json_ev = '/audio_mamba/data/eval/a.json'
output_json_ev = '/audio_mamba/data/eval/circor_eval.json'


# Function to update the wav path
def update_wav_path(wav,new_path) :
    filename = wav.split('/')[-1]  # Get the filename from the path
    return new_path + filename

# Read the input JSON file
with open(input_json, 'r') as f:
    input_data = json.load(f)

# Update the wav path for each entry
for entry in input_data:
    entry['wav'] = update_wav_path(entry['wav'], new_directory_path)

# Convert to the desired format
output_data = {"data": input_data}


# Write the output JSON file
with open(output_json) as f:
    json.dump(output_data, f, indent=4)

print("Conversion complete. Output written to output.json")

#############################################################

# Read the input JSON file
with open(input_json_ev, 'r') as f:
    input_data = json.load(f)

# Update the wav path for each entry
for entry in input_data:
    entry['wav'] = update_wav_path(entry['wav'], new_directory_path_ev)

# Convert to the desired format
output_data = {"data": input_data}


# Write the output JSON file
with open(output_json_ev) as f:
    json.dump(output_data, f, indent=4)


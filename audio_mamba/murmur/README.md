# SSAMBA: Self-Supervised Audio Mamba


## Introduction
This repository contains the official implementation (in PyTorch) of the the paper SSAMBA: Self-Supervised Audio Representation Learning with Mamba State Space Model. SSAMBA is an advanced audio representation learning model designed to leverage self-supervised learning techniques using the Mamba State Space Model. This project builds on the success of the Self-Supervised Audio Spectrogram Transformer (SSAST) and introduces novel methodologies to further enhance performance and efficiency on various audio tasks. 

## Installation

To install the necessary dependencies, you can use the following commands:

Python version: 3.10.13
pytorch Cuda version 11.8 
Torch 2.1.1 

pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118


```bash
cd pre_trained_mamba
git clone https://github.com/SiavashShams/ssamba.git
cd ssamba
pip install -r requirements.txt
cd src
git clone https://github.com/hustvl/Vim.git
pip install -r /Vim/vim/vim_requirements.txt
```


## Pretraining

We pretrained SSAMBA with various sizes (base, small, tiny) for patches (250, 300, and 400) on a mixture of unlabeled audios from AudioSet and LibriSpeech. You can find these weights in the "Pretrained Model Weights" section below. However, if you want to pretrain the model from scratch, follow this recipe:

1. **Navigate to the Directory**: Change to the directory containing the pretraining scripts. You can do this by running the following command in your terminal:
    ```bash
    cd ssamba/src/pretrain/murmur
    ```

2. **Adjust the Script**: Edit the `run_mask_patch_amba.sh` script to update the paths to your data files:
Change the following paths to the corresponding ones for the server that is running the model:

Run_mask_patch_amba.sh:
tr_data=/home/icsl/Documents/adrian/classification/pre_trained_mamba/data/train/circor_train.json
te_data=/home/icsl/Documents/adrian/classification/pre_trained_mamba/data/eval/circor_test.json
--label-csv /home/icsl/Documents/adrian/classification/pre_trained_mamba/class_labels_indices.csv 

Run_amba.py:
```bash

sys.path.append('/home/icsl/Documents/adrian/classification/pre_trained_mamba/ssamba')
```


Both_models.py: 
```bash
sys.path.append('/home/icsl/Documents/adrian/classification/pre_trained_mamba/ssamba/src/Vim')
sys.path.append('/home/icsl/Documents/adrian/classification/pre_trained_mamba/ssamba/src/Vim/vim')
sys.path.append('/home/icsl/Documents/adrian/classification/pre_trained_mamba/ssamba/src/Vim/mamba-1p1p1s')
``` 

2a. **Adjust Json files**: Edit the 'audio_mamba/murmur/adjust_json.py' scripte to update the paths to the data files:
Include path to audio_mamba before each of specified paths
```bash
new_directory_path = "/audio_mamba/data/train/"
input_json = '/audio_mamba/data/train/a.json'
output_json = '/audio_mamba/data/train/circor_train.json'

new_directory_path_ev = "/audio_mamba/data/eval/"
input_json_ev = '/audio_mamba/data/eval/a.json'
output_json_ev = '/audio_mamba/data/eval/circor_eval.json'

```

then run the adjust_json.py script 

3. **Run the Script**: After making the necessary adjustments, execute the script to start the pretraining process. You can run the script directly from the terminal with the following command (from path ssamba/src/pretrain/murmur):
    ```bash
    ./run_mask_patch_amba.sh
    ```

## Pretrained Model Weights

The pretrained model weights for our SSAMBA model in sizes (base, small, and tiny) for different number of masked patches (400, 300, 250) can be found at:

[Pretrained Model Weights](https://drive.google.com/drive/u/1/folders/1E1gf5SxdSByDJ16_WQvzTKn8lIoYtZiX)

## Finetuning
TODO: Add finetune datasets 
To finetune the pretrained SSAMBA on the balanced earbud recording dataset, follow these steps:

1. **Navigate to the finetuning directory:**
   - For Audioset:
     ```bash
     cd audio_mamba/murmur/finetune directory
     ```
   

2. **Adjust the paths and hyperparameters:**
   Edit `run_cir_amba.sh` in the audio_mamba/murmur/finetune directory. Adjust the paths and hyperparameters as needed for your dataset.


3. **Run the job submission script:**
   Execute the `run_cir_amba.sh` script in the terminal to start the finetuning process:
   ```bash
   ./run_cir_amba.sh
   ```


### Step 2: Prepare the Fine-Tuning Scripts

1. **Copy our files**:
   - Copy the files from `src/finetune/voxceleb1/ssast` to `s3prl/s3prl/upstream/ssast`.

### Step 3: Adjust Paths and Specify Models

1. **Edit the `run_sid.sh` file**:
   - Adjust the paths in the `run_sid.sh` file to point to the correct directories for your dataset and model.

2. **Specify models in `submit_jobs_amba.sh`**:
   - Edit the `submit_jobs_amba.sh` script to specify the models you want to fine-tune.

### Step 4: Run the Fine-Tuning Script

1. **Execute the `submit_jobs_amba.sh` script**:
   - In the terminal, navigate to the directory containing `submit_jobs_amba.sh` and run:
     ```bash
     ./submit_jobs_amba.sh
     ```



## License
The license for borrowed code can be found in [LICENSE](https://github.com/SiavashShams/ssamba/blob/main/LICENSE) file. 
We acknowledge the wonderful work of [SSAST](https://arxiv.org/abs/2110.09784), and [Vision Mamba](https://arxiv.org/abs/2401.09417). 

## Citing
If you find this work helpful, please consider giving us a star 🌟 and citing:

```bibtex
@article{shams2024ssamba,
      title={SSAMBA: Self-Supervised Audio Representation Learning with Mamba State Space Model},
      author={Siavash Shams and Sukru Samet Dindar and Xilin Jiang and Nima Mesgarani},
      year={2024},
      eprint={2405.11831},
      archivePrefix={arXiv},
      primaryClass={eess.AS},
      journal={arXiv preprint arXiv:2405.11831}
}

```

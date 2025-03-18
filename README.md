# Overview
This a baseball statistics prediction model created by me. There is the core source file for model creation in the ```src/``` folder. There is also an api and sql files in the ```api``` folder. The reason for the api and database creation is to add more training data not found in the pybaseball csvs and make the querying for single player prediction easier. 

# Project Structure
- src/: The src folder contains the python source files for model creation and training.
- scripts/: The scripts folder contains the bash script files that can be used for training and evluating models. 
- api/: The spi folder contains the go and sql files for the API. 

# Model Creation Steps
```bash
conda create -n statsmodel 
conda activate statsmodel
conda install pytorch torchvision -c pytorch
git clone https://github.com/ggarcia453/Baseball-Stats-Predictor
cd Baseball-Stats-Predictor/
pip install -r requirements.txt
wandb login
```

# Script Overview
This section gives a brief overview of the variosu shell scripts included in this repository.

## Train New
This script will create a new machine learning model. The Bash variables are explained below. 

| Variable    | Explaination |
| -------- | ------- |
| PYTHONSRCPATH | Path to main python driver file.   |
| EPOCHNUM | Number of epochs to use. |
| b_p | Sets mode to either batting or pitching. | 
| start_year | Sets the start year for stats that are considered for training the model. | 
| end_year | Sets the end year for stats that are considered for training the model. | 
| model_dicretory| Sets the directory where the model is saved. |
| data_mode | Sets the method for obtaining data. |
| use_wandb | Determines if stats are logged to wandb. | 

## Eval Model
This script will evaluate the model. If a directory with multiple models is provided, it will grab the best performing as determined by loss. The Bash variables are explained below. 
| Variable    | Explaination |
| -------- | ------- |
| PYTHONSRCPATH | Path to main python driver file.   |
| b_p | Sets mode to either batting or pitching. MUST BE SET TO APPROPIATE MODE FOR TRAINING TO OBTAIN RIGHT DATA. | 
| start_year | Sets the start year for stats that are considered for evaluating the model. | 
| end_year | Sets the end year for stats that are considered for evaluating the model. | 
| model_dicretory| The directory from where the model is loaded from. |

## Predict Player
This script will take a model and a player's stats then predict the final stat. 

| Variable    | Explaination |
| -------- | ------- |
| PYTHONSRCPATH | Path to main python driver file.   |
| b_p | Sets mode to either batting or pitching. MUST BE SET TO APPROPIATE MODE FOR TRAINING TO OBTAIN RIGHT DATA. | 
| model_dicretory| The directory from where the model is loaded from. |
| name | Name for player. Seperate first and last name with space. |
| year | Year for predictions. |

## How to use scripts
These scripts are intended to be run from the root project directory. This means that you should run it as follows:
```bash
bash scripts/train-new.sh
# or 
./scripts/train-new.sh
```
Train new should be run before ``` predict-player.sh``` and ```eval-model.sh```.

# Wandb Reports
Here is an archive of basic wandb reports of models I have created. \
[Dec. 7, 2024](https://api.wandb.ai/links/gegarci1/w64wg81f)

# Future Plans
1. Enhance model architecture for better accuracy.
2. Integrate data from additional sources via web scraping.
3. Expand API capabilities for greater flexibility.
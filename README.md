# Overview
This a baseball statistics prediction model created by me. There is the core source file for model creation in the ```src/``` folder. There is also an api and sql files in the ```api``` folder. The reason for the api and database creation is to add more training data not found in the pybaseball csvs and make the querying for single player prediction easier. 

# Model Creation Steps
```bash
conda create -n statsmodel 
conda activate statsmodel
conda install pytorch torchvision -c pytorch
git clone https://github.com/ggarcia453/Baseball-Stats-Predictor
cd Baseball-Stats-Predictor/
pip install -r requirements.txt
./train-new.sh
```

# Database Setup
Install postgres via one of two methods
1. [Official download/Package Managers](https://www.postgresql.org/download/)
2. [Installaiation via downloading files without package manager](https://gist.github.com/yunpengn/832aceac6998e2f894e5780229920cb5)

For method 1, run 
```bash
./postgres_setup.sh
```

For method 2 you will have to follow the setup guide linked to start the server then run the script. 

# Future Plans
1. Further refine API to allow for querys for batters
2. Complete model evaluation and model prediction features.
3. Begin working on pitcher database/api
4. Continue tinkering model to minimize loss
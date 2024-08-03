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

# TODO
1. Create REST API to remove dependence on pybaseball/local files + add more datapoints
2. Generalize model for inference/prediction 
3. Continue tinkering model to minimize loss
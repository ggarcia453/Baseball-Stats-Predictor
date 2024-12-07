#! /bin/bash
PYTHONSRCPATH=src/main.py
b_p=batting #should be either batting or pitching
model_directory=models/AVG-HR-OPS-RAR-wRC+-WAR
EVAL=false
## For evaluation purposes
b_p=batting #should be either batting or pitching
start_year=1940
end_year=2023

if [ ! -d "$model_directory" ]; then
  echo "$model_directory does not exist."
  exit 1
fi

python3 $PYTHONSRCPATH -m $b_p  -lm $model_directory -ev -m  $b_p -y $start_year"_"$end_year -ple

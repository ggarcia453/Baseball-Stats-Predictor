#! /bin/bash
PYTHONSRCPATH=src/main.py
b_p=batting #should be either batting or pitching
model_directory=models/AVG-BABIP-G-HR-K%-RAR-wRC+-WAR
## For evaluation purposes
b_p=batting #should be either batting or pitching
start_year=2010
end_year=2024

if [ ! -d "$model_directory" ]; then
  echo "$model_directory does not exist."
  exit 1
fi

python3 $PYTHONSRCPATH -lm $model_directory -ev -m  $b_p -y $start_year"_"$end_year -ple

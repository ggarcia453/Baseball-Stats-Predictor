#! /bin/bash
PYTHONSRCPATH=src/main.py
EPOCH_NUM=100
b_p=batting #should be either batting or pitching
start_year=1945
end_year=2023
model_directory=models
data_mode=csv #should be either csv or pyb or api

echo $b_p"_data_"$start_year"_"$end_year

python3 $PYTHONSRCPATH -m  $b_p -y $start_year"_"$end_year -dm $data_mode -i AVG HR RAR OPS wRC+ -o WAR -e $EPOCH_NUM -sm $model_directory

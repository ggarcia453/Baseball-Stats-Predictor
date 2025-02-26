#! /bin/bash
PYTHONSRCPATH=src/main.py
EPOCH_NUM=1000
b_p=batting #should be either batting or pitching
start_year=1990
end_year=2024
model_directory=models
data_mode=api #should be either csv or pyb or api
use_wandb=true # should be either true or false

echo $b_p"_data_"$start_year"_"$end_year

if [ "$use_wandb" = true ] ; then
    python3 $PYTHONSRCPATH -m  $b_p -y $start_year"_"$end_year -dm $data_mode -i G RAR AVG wRC+ BABIP K% HR -o WAR -e $EPOCH_NUM -sm $model_directory -w
else
    python3 $PYTHONSRCPATH -m  $b_p -y $start_year"_"$end_year -dm $data_mode -i wRC+ BABIP K% G -o WAR -e $EPOCH_NUM -sm $model_directory
fi

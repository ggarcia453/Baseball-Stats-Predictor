#! /bin/bash
PYTHONSRCPATH=src/main.py
CSV=true
EPOCH_NUM=250
b_p=batting #should be either batting or pitching
start_year=1945
end_year=2023
model_directory=models

echo $b_p"_data_"$start_year"_"$end_year


if [ "$CSV" = true ] ; then
    python3 $PYTHONSRCPATH -m  $b_p -y $start_year"_"$end_year -c -i AVG HR OPS wRC+ wOBA -o WAR -e $EPOCH_NUM -sm $model_directory
else
   python3 $PYTHONSRCPATH -d $b_p"_data_"$start_year"_"$end_year -i  AVG HR RAR OPS wRC+ -o WAR -e $EPOCH_NUM -sm $model_directory 
fi

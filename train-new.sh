#! /bin/bash
PYTHONSRCPATH=src/main.py
CSV=true
EPOCH_NUM=100
b_p=batting #should be either batting or pitching
start_year=1969
end_year=2019

echo $b_p"_data_"$start_year"_"$end_year


if [ "$CSV" = true ] ; then
    python3 $PYTHONSRCPATH -d $b_p"_data_"$start_year"_"$end_year -c -i RAR OPS AVG wRC+ -o WAR -sm -e $EPOCH_NUM
else
    python3 $PYTHONSRCPATH -i RAR -e $EPOCH_NUM
fi

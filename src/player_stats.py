"""
Python Module for various statistics loading.
"""
import os
import requests
from pybaseball import pitching_stats, batting_stats, playerid_lookup, cache
import torch
import tqdm
import pandas

cache.enable()

class ValidationError(Exception):
    """
    Class for Validation Errors. To be used when dataset is not valid.
    """

def get_dataset(dataset:str):
    """
    Takes in a dataset string and returns the stat set as requested. 
    """
    x = dataset.split("_")
    p_b, _, start, end  = x
    if p_b == "pitching":
        return pitching_stats(start, end)
    if p_b == "batting":
        return batting_stats(start, end)
    raise ValueError("Not valid stat set")


def validate_dataset(args, dataset):
    """
    Tests that dataset is valid before returning it. 
    """
    assert isinstance(dataset, pandas.DataFrame), 'Should be Pandas Dataframe'
    dataset = dataset[args.input_args]
    try:
        assert (dataset.columns.values[0] == args.output_args), "Something is wrong with dataset"
    except AssertionError:
        dataset.insert(0, args.output_args, dataset.pop(args.output_args))
    return dataset


def df_tensor_convert(data):
    """
    Helper function to convert data into torch tensor of floats. 
    """
    return torch.from_numpy(data.values).float()



def dataset_loader(args):
    """Load dataset from csv, pybaseball or api as requested"""
    download = True
    s = args.save_csv
    if (args.mode in ["batting", "pitching"]):
        path = f"{args.mode}_data/{args.mode}_data_{args.year_range}"
        parentpath = f"{args.mode}_data/"
    else:
        raise ValidationError("Not valid Set")
    match (args.data_mode):
        case "csv":
            try:
                dataset = pandas.concat([chunk for chunk in
                    tqdm.tqdm(pandas.read_csv(path + ".csv", chunksize=1000), desc='Loading data')])
                download = False
            except FileNotFoundError:
                print("No csv found in current directory\n"
                      +"Dowlnloading and saving data from FanGraphs")
                s = True
        case "pyb":
            download = True
        case "api":
            print(args.year_range, args.mode)
            y1, y2 = args.year_range.split("_")
            link = f"http://localhost:8080/{args.mode}?&Season={y1}&Season={y2}"
            list_response = requests.get(link, timeout=10).json()
            if list_response is None:
                print("Could not access data")
                download = True
            else:
                all_keys = {key for entry in list_response for key in entry.keys()}
                filtered_data = []
                for entry in list_response:
                    processed_entry = {}
                    for key in all_keys:
                        if key in entry and entry[key]["Valid"]:
                            processed_entry[key] = entry[key][next(iter(entry[key]))]
                        else:
                            processed_entry[key] = None
                    filtered_data.append(processed_entry)
                dataset = pandas.DataFrame(filtered_data)
                download = False
        case i:
            print(i)
            download = True
    if download:
        dataset = get_dataset(f"{args.mode}_data_{args.year_range}")
    print("Loaded")
    if s:
        if not os.path.isdir(parentpath):
            os.makedirs(parentpath)
        dataset.to_csv(f"{path}.csv")
        print("saved to csv")
    return dataset

def grabid(player):
    """
    Takes player string and returns associated pybaseball id. 
    """
    return playerid_lookup(*player)

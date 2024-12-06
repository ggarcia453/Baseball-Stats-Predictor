from pybaseball import pitching_stats, batting_stats, playerid_lookup, cache
import torch, pandas, tqdm, os

cache.enable()

class ValidationError(Exception):
    pass

def get_dataset(dataset):
    x = dataset.split("_")
    p_b, _, start, end  = x
    if p_b == "pitching":
        return pitching_stats(start, end)
    elif p_b == "batting":
        return batting_stats(start, end)
    else:
        raise ValueError("Not valid stat set")
    

def validate_dataset(args, dataset):
    assert type(dataset) == pandas.DataFrame, f'Should be Pandas Dataframe'
    dataset = dataset[args.input_args]
    try:
        assert (dataset.columns.values[0] == args.output_args), "Something is wrong with dataset"
    except AssertionError: 
        dataset.insert(0, args.output_args, dataset.pop(args.output_args))
    return dataset
    
    
def df_tensor_convert(data):
    return torch.from_numpy(data.values).float()



def dataset_loader(args):
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
                dataset = pandas.concat([chunk for chunk in tqdm.tqdm(pandas.read_csv(path + ".csv", chunksize=1000), desc='Loading data')])
                download = False
            except FileNotFoundError: 
                print("No csv found in current directory\nDowlnloading and saving data from FanGraphs")
                s = True
        case "pyb":
            download = True
        case "api":
            print(args.year_range, args.mode)
            raise ValidationError
        case i :
            print(i)    
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
    return playerid_lookup(*player)


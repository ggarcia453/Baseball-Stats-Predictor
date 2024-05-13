from pybaseball import pitching_stats, batting_stats
import torch, pandas, numpy

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
    rlist = [i for i in list(dataset.columns.values) if i not in args.input_args]
    dataset = dataset.drop(rlist,axis=1).dropna()
    try:
        assert (dataset.columns.values[0] == 'WAR'), "Something is wrong with dataset"
    except AssertionError: 
        dataset.insert(0, 'WAR', dataset.pop('WAR'))
    return dataset
    
    
def df_tensor_convert(data):
    d = {}
    for i in data.columns.values:
        d[i] = torch.Tensor(data[i])
    return d



def dataset_loader(args):
    print("Loading data...")
    download = True
    s = args.save
    match args.dataset.split("_")[0]:
        case "batting":
            path = "batting_data/" + args.dataset
        case "pitching":
            path = "pitching_data/" + args.dataset
        case _:
            raise ValidationError("Not valid Set")
    if args.from_csv:
        try:
            dataset = pandas.read_csv(path + ".csv").drop('Unnamed: 0', axis=1)
            download = False
        except FileNotFoundError: 
            print("No csv found in current directory\nDowlnloading and saving data from FanGraphs")
            s = True
    if download:
        dataset = get_dataset(args.dataset)
    print("Loaded")
    if s:
        dataset.to_csv(f"{path}.csv")
        print("saved to csv")
    return dataset
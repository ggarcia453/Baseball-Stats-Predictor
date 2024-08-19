import argparse,sys, torch
from model import baseball_model
from player_stats import get_dataset, validate_dataset, dataset_loader

def grab_inputs(args):
    args.input_args = "".join(args.load_model.split("/")[1:]).split("-")
    return args

def main():
    parser = argparse.ArgumentParser(description='Main function for training baseball_models')
    data_pipeline = parser.add_argument_group('Input and Output Pipeline')
    data_pipeline.add_argument('-d', '--dataset', default='batting_data_2000_2019', help='Dataset to use for training. Use format [batting|pitching]_data_[starting year]_[ending year]')
    parser.add_argument('-l', '--learning_rate', default=0.00005, help="Base learning rate. (Will decrease in model to prevent exploding gradient)")
    parser.add_argument('-e', '--epochs', default=2500, help="Number of epochs for training")
    parser.add_argument('-c', '--from_csv', action='store_true', help='Load data from CSV instead of fangraphs website')
    parser.add_argument('-sc', '--save_csv', action='store_true', help='Save data in csv file ')
    parser.add_argument('-lm', '--load_model', help='Load model from a model directory')
    parser.add_argument('-sm', '--save_model', help="Save best performing model in directory")
    parser.add_argument('-pp', '--predict_player', help='After training or loading model, predict stat for certain player')
    parser.add_argument('-rt', '--retrain', action='store_true', help='Only with loading model, Trains loaded modela nd overwrites if better. ')
    data_pipeline.add_argument('-o', '--output_args', default='WAR', help='Stat to be predicted')
    data_pipeline.add_argument('-i', '--input_args', nargs='+',default=['RAR'], help="Stats that are used for prediction")
    args = parser.parse_args()
    if args.load_model:
        args = grab_inputs(args)
        model = baseball_model(args)
        with open(f"{args.load_model}/best-loss.txt") as f:
            name = f.readlines()[1].strip()
        model.load_state_dict(torch.load(f"{args.load_model}/{name}.pt"))
        print(f"model at {args.load_model} loaded")
        if args.retrain:
            pass
        else:
            model.predict(args.predict_player)
    else:
        print('Validating Input Output Args')
        #TODO Validate Input Output args
        dataset = dataset_loader(args)   
        args.input_args += [args.output_args] 
        print("Validating Dataset")
        inputs = validate_dataset(args, dataset)
        if len(inputs) == 0:
            raise RuntimeError("No Dataset points identified ")
        print(f"Validated! Using {len(inputs)} dataset points")
        model = baseball_model(args)
        if (model.dims == 1):
            raise RuntimeError("Model not initialzed correctly")
        print(f"Created {model}")
        count = 0
        while count < 10:
            try:
                model.train(args.epochs, args.learning_rate, args.output_args, inputs)
                break
            except ValueError:
                model = baseball_model(args)
                print("NAN loss. New model created")
                count +=1
        
        if args.save_model:
            model.save(args.save_model)
    print("Completed")

if __name__ == "__main__":
    main()
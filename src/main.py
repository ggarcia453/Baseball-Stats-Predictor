import argparse,sys, torch
from model import baseball_model
from player_stats import get_dataset, validate_dataset, dataset_loader

def grab_inputs(args):
    args.input_args = "".join(args.load_model.split("/")[1:]).split("-")
    return args

def main():
    parser = argparse.ArgumentParser(description='Main function for training baseball_models')
    data_pipeline = parser.add_argument_group('Input and Output Pipeline')
    data_pipeline.add_argument('-m', '--mode', default='batting', help='Mode for use. Should be either \'batting\' or \'pitching\'')
    data_pipeline.add_argument('-y', '--year_range', default='2000_2019', help='Year Range for use for traning')
    parser.add_argument('-l', '--learning_rate', default=0.00005, help="Base learning rate. (Will decrease in model to prevent exploding gradient)")
    parser.add_argument('-e', '--epochs', default=2500, help="Number of epochs for training")
    parser.add_argument('-c', '--from_csv', action='store_true', help='Load data from CSV instead of fangraphs website')
    parser.add_argument('-sc', '--save_csv', action='store_true', help='Save data in csv file ')
    parser.add_argument('-lm', '--load_model', help='Load model from a model directory')
    parser.add_argument('-sm', '--save_model', help="Save best performing model in directory")
    parser.add_argument('-pp', '--predict_player', help='After training or loading model, predict stat for certain player')
    parser.add_argument('-ev', '--eval', action='store_true', help='Only with loading model, Runs an evaluation of performance')
    parser.add_argument('-ple', '--plot_eval', action='store_true', help='Plot evaluation Predictions')
    data_pipeline.add_argument('-o', '--output_args', default='WAR', help='Stat to be predicted')
    data_pipeline.add_argument('-i', '--input_args', nargs='+',default=['RAR'], help="Stats that are used for prediction")
    args = parser.parse_args()
    if args.load_model:
        args = grab_inputs(args)
        model = baseball_model(args)
        with open(f"{args.load_model}/best-loss.txt") as f:
            name = f.readlines()[1].strip()
        model.load_state_dict(torch.load(f"{args.load_model}/{name}.pt", weights_only=False))
        print(f"model at {args.load_model} loaded")
        model.eval()
        if args.eval:
            dataset = dataset_loader(args)   
            print("Validating Dataset")
            inputs = validate_dataset(args, dataset)
            if len(inputs) == 0:
                raise RuntimeError("No Dataset points identified ")      
            if args.plot_eval:      
                model.evaluation(inputs, args.plot_eval)
            else:
                model.evaluation(inputs)
        else:
            data = model.data_fetch(args.predict_player, args.mode)
            data = data.unsqueeze(0)
            print(data)
            with torch.no_grad():
                print(model(data)[0])
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
        model.train_model(args.epochs, args.learning_rate, inputs, 0.01)
        if args.save_model:
            model.save(args.save_model)
    print("Completed")

if __name__ == "__main__":
    main()
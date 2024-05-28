import argparse
from model import baseball_model
from player_stats import get_dataset, validate_dataset, dataset_loader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Main function for training baseball_models')
    data_pipeline = parser.add_argument_group('Input and Output Pipeline')
    parser.add_argument('-d', '--dataset', default='batting_data_2000_2019', help='Dataset to use for training. Use format [batting|pitching]_data_[starting year]_[ending year]')
    parser.add_argument('-l', '--learning_rate', default=0.0001, help="Base learning rate. (Will decrease in model to prevent exploding gradient)")
    parser.add_argument('-e', '--epochs', default=2500, help="Number of epochs for training")
    parser.add_argument('-c', '--from_csv', action='store_true', help='Load data from CSV instead of fangraphs website')
    parser.add_argument('-sc', '--save_csv', action='store_true', help='Save data in csv file ')
    parser.add_argument('-lm', '--load_model', help='Load model from a model directory')
    parser.add_argument('-sm', '--save_model', action='store_true', help="Save best performing model in directory")
    data_pipeline.add_argument('-o', '--output_args', default='WAR', help='Stat to be predicted')
    data_pipeline.add_argument('-i', '--input_args', nargs='+', required=True, help="Stats that are used for prediction")
    args = parser.parse_args()
    dataset = dataset_loader(args)   
    args.input_args += [args.output_args] 
    print("Validating Dataset")
    inputs = validate_dataset(args, dataset)
    if len(inputs) == 0:
        raise RuntimeError("No Dataset points identified ")
    print(f"Validated! Using {len(inputs)} dataset points")
    model = baseball_model(len(inputs.columns.values)-1)
    if (model.dims == 1):
        raise RuntimeError("Model not initialzed correctly")
    print(f"Created {model}")
    model.train(args.epochs, args.learning_rate, args.output_args, inputs)
    if args.save_model:
        model.save()
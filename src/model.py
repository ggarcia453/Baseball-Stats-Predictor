"""
Python Module for Baseball Statistics Predictor Model. 
"""
from copy import deepcopy
import os
import uuid
import torch
import requests
from torch.autograd import Variable
from torch import optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import r2_score, root_mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
import wandb
from player_stats import df_tensor_convert

class SearchError(Exception):
    """
    Search Error Class. 
    Used when not able to find a partivular player.
    """

class BaseballModel(torch.nn.Module):
    """
    Baseball Model Class. 
    """
    def __init__(self, args, dropout_rate=0.2):
        super().__init__()
        input_dim = len(args.input_args)-1
        sizes = [input_dim, 4 * input_dim, 8 * input_dim, 4 * input_dim,
                 4 *input_dim, 2 * input_dim, 2 * input_dim, input_dim]  # Increased layer sizes
        layers = []
        prev_size = input_dim
        for _, hidden_size in enumerate(sizes):
            layers.append(torch.nn.Linear(prev_size, hidden_size))
            layers.append(torch.nn.ReLU())
            layers.append(torch.nn.Linear(hidden_size, hidden_size))
            layers.append(torch.nn.BatchNorm1d(hidden_size))
            layers.append(torch.nn.Dropout(dropout_rate))
            prev_size = hidden_size
        self.hidden_layers = torch.nn.Sequential(*layers)
        self.output = torch.nn.Linear(input_dim, 1)
        self.dims = input_dim + 1
        self.stats = args.input_args
        self.loss = float('inf')
        self.best = None
        self.y_mean = None
        self.y_std = None

    def forward(self, x):
        """
        Forward move for learning. 
        """
        out = self.hidden_layers(x)
        return self.output(out)

    def set_normalization_params(self, y_mean, y_std):
        """
        Set normalization parameters for use later. 
        """
        self.y_mean = y_mean
        self.y_std = y_std

    def denormalize_output(self, normalized_output):
        """Return denomalized input."""
        return (normalized_output * self.y_std) + self.y_mean

    def save(self, directory):
        """Saves model to pt. file."""
        if not os.path.isdir(directory):
            print("Creating directory")
            os.makedirs(directory)
        output = self.stats[-1]
        del self.stats[-1]
        name = uuid.uuid4()
        folder = f"{directory}/{'-'.join(sorted(self.stats))}-{output}"
        if not os.path.exists(folder):
            os.makedirs(folder)
            torch.save(self.best, f"{folder}/{name}.pt")
            with open(f"{folder}/best-loss.txt", "w", encoding="UTF-8") as f:
                f.write(str(self.loss))
                f.write("\n" + str(name))
            print(f"Saved to new folder {folder}")
        else:
            with open(f"{folder}/best-loss.txt", "r", encoding="UTF-8") as f:
                t = float(f.readlines()[0].strip())
            torch.save(self.best, f"{folder}/{name}.pt")
            if t > self.loss:
                with open(f"{folder}/best-loss.txt", "w", encoding="UTF-8") as f:
                    f.write(f"{str(self.loss)}\n{name}")

    @staticmethod
    def _prepare_data(df, batch_size=32):
        y = df[:,0]
        x = df[:,1:]
        x_mean = x.mean(axis=0)
        x_std = x.std(axis=0)
        x_normalized = (x - x_mean) / (x_std + 1e-8)
        y_mean = y.mean()
        y_std = y.std()
        y_normalized = (y - y_mean) / (y_std + 1e-8)
        x_train, x_val, y_train, y_val = train_test_split(x_normalized,
            y_normalized, test_size=0.2, random_state=42)
        x_train_tensor = x_train.clone().detach().float()
        y_train_tensor = y_train.clone().detach().float()
        x_val_tensor = x_val.clone().detach().float()
        y_val_tensor = y_val.clone().detach().float()
        train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
        val_dataset = TensorDataset(x_val_tensor, y_val_tensor)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        return train_loader, val_loader, (x_mean, x_std, y_mean, y_std)

    def train_model(self, epochs, learning_rate, data, use_wandb, l2_lambda=0.0):
        """
        Training method.
        """
        train_loader, val_loader, (_x_mean, _x_std, y_mean, y_std) = self._prepare_data(
            df_tensor_convert(data))
        self.set_normalization_params(y_mean, y_std)
        criterion = torch.nn.MSELoss()
        optimizer = optim.Adam(self.parameters(), lr=learning_rate, weight_decay=l2_lambda)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min',
            patience=5, factor=0.5, verbose=True)
        print("Training")
        for epoch in range(int(epochs)):
            self.train()  # Set model to training mode
            total_loss = 0.0
            for inputs, labels in train_loader:
                optimizer.zero_grad()
                outputs = self.forward(inputs)
                # get loss for the predicted output
                loss = criterion(outputs, labels.view(-1, 1))
                if torch.isnan(loss):
                    raise ValueError("NAN loss")
                # get gradients w.r.t to parameters
                if self.loss > loss.item():
                    print("Updated")
                    self.loss = loss.item()
                    self.best = deepcopy(self.state_dict())
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            val_loss, val_min, val_max = self.validate_self(val_loader, criterion)
            avg_loss = total_loss / len(train_loader)
            scheduler.step(val_loss)  # Adjust learning rate based on validation loss
            val_min_denorm = self.denormalize_output(torch.tensor(val_min)).item()
            val_max_denorm = self.denormalize_output(torch.tensor(val_max)).item()
            print(f'Epoch {epoch + 1}, Train Loss: {avg_loss:.4f}, Val Loss: {val_loss:.4f}, '
              f'Val Range: [{val_min_denorm:.4f}, {val_max_denorm:.4f}]')
            evalres = self.evaluation(data)
            if use_wandb:
                wandb.log({
                "train_loss": avg_loss / len(train_loader),
                "val_loss": val_loss,
                "mse" : evalres["mse"], 
                "r2" : evalres["r2"]
                })
        print(f'Minimum loss {self.loss}')

    def data_fetch_player(self, player_year:str, mode:str):
        """
        Fetches Data from api for prediction.
        """
        first, last, year = player_year.split(" ")
        link = f"http://localhost:8080/{mode}?Name={first}-{last}&Season={year}"
        list_response = requests.get(link, timeout=10).json()
        if list_response is None:
            raise SearchError(f"Could not find player {first} {last}. "+
                        f"Check for spelling and that the model is for pitching or batting\n{link}")
        keys = {y : x for x,y  in list(enumerate(self.stats))}
        valu = {x:list(y.values())[0] for x,y in list_response[0].items()
                if x in self.stats[:-1] and y['Valid']}
        tensor = Variable(torch.Tensor([i for _, i  in sorted(list(valu.items()),
                key= lambda x: keys[x[0]])]))
        return tensor

    def validate_self(self, val_loader, criterion):
        """
        Validation method. called during training. 
        """
        self.eval()
        total_loss = 0.0
        all_preds = []
        with torch.no_grad():
            for data, target in val_loader:
                output = self(data)
                loss = criterion(output, target.view(-1,1))
                total_loss += loss.item()
                all_preds.extend(output.tolist())
        avg_loss = total_loss / len(val_loader)
        return avg_loss, min(all_preds), max(all_preds)

    def predict(self, input_data):
        """
        Prediction method. Used in predict-player script.
        """
        self.eval()
        with torch.no_grad():
            normalized_output = self(input_data)
            return self.denormalize_output(normalized_output)

    def evaluation(self, data, print_res=False, ple=False):
        """
        Evaluation method. Used in eval-model script. 
        """
        _, test_loader, (_,_, y_mean, y_std) = self._prepare_data(df_tensor_convert(data))
        self.set_normalization_params(y_mean, y_std)
        self.eval()
        all_predictions = []
        all_targets = []

        with torch.no_grad():
            for inputs, targets in test_loader:
                outputs = self(inputs)
                all_predictions.extend(self.denormalize_output(outputs).numpy().flatten())
                all_targets.extend(self.denormalize_output(targets.view(-1,1)).numpy().flatten())
        all_predictions = np.array(all_predictions)
        all_targets = np.array(all_targets)
        mse = mean_squared_error(all_targets, all_predictions)
        rmse = root_mean_squared_error(all_targets, all_predictions)
        mae = mean_absolute_error(all_targets, all_predictions)
        r2 = r2_score(all_targets, all_predictions)
        errors = all_predictions - all_targets
        mean_error = np.mean(errors)
        median_error = np.median(errors)
        error_std = np.std(errors)
        percentile_errors = np.percentile(np.abs(errors), [25, 50, 75, 90, 95])
        if print_res:
            print("Evaluation Results:")
            print(f"Mean Squared Error (MSE): {mse:.4f}")
            print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
            print(f"Mean Absolute Error (MAE): {mae:.4f}")
            print(f"R-squared (R2) Score: {r2:.4f}")
            print(f"Mean Error: {mean_error:.4f}")
            print(f"Median Error: {median_error:.4f}")
            print(f"Standard Deviation of Error: {error_std:.4f}")
            print(f"25th Percentile of Absolute Error: {percentile_errors[0]:.4f}")
            print(f"50th Percentile (Median) of Absolute Error: {percentile_errors[1]:.4f}")
            print(f"75th Percentile of Absolute Error: {percentile_errors[2]:.4f}")
            print(f"90th Percentile of Absolute Error: {percentile_errors[3]:.4f}")
            print(f"95th Percentile of Absolute Error: {percentile_errors[4]:.4f}")
        if ple:
            plt.figure(figsize=(10, 6))
            plt.scatter(all_targets, all_predictions, alpha=0.5)
            plt.plot([min(all_targets), max(all_targets)],
                [min(all_targets), max(all_targets)], 'r--', lw=2)
            plt.xlabel("Actual Values")
            plt.ylabel("Predicted Values")
            plt.title("Actual vs Predicted Values")
            plt.show()
        return {
            "mse": mse,
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
            "mean_error": mean_error,
            "median_error": median_error,
            "error_std": error_std,
            "percentile_errors": percentile_errors
        }


    def __str__(self):
        return f"Baseball model with {self.dims - 1} input dimension"

import torch, numpy, json, os, uuid, requests
from torch.autograd import Variable
from player_stats import df_tensor_convert
from copy import deepcopy
import torch.optim as optim


class SearchError(Exception):
    pass

class baseball_model(torch.nn.Module):
    def __init__(self, args, dropout_rate=0.2):
        super(baseball_model, self).__init__()
        inputDim = len(args.input_args)-1
        sizes = [inputDim, 2 * inputDim, 4 * inputDim, 2 * inputDim, inputDim]
        layers = []
        prev_size = inputDim
        for i, hidden_size in enumerate(sizes):
            layers.append(torch.nn.Linear(prev_size, hidden_size))
            if i % 2 == 0:
                layers.append(torch.nn.Tanh()) 
            else:
                layers.append(torch.nn.LeakyReLU())  
            layers.append(torch.nn.BatchNorm1d(hidden_size))
            layers.append(torch.nn.Dropout(dropout_rate))
            prev_size = hidden_size
        self.hidden_layers = torch.nn.Sequential(*layers)
        self.output = torch.nn.Linear(inputDim, 1)
        self.dims = inputDim + 1
        self.stats = args.input_args
        self.loss = float('inf')
        self.best = None
        
    def forward(self, x):
        out = self.hidden_layers(x)
        out = self.output(out)
        return out
    
    def normalize(self, arr, name):
        a,i = torch.max(arr), torch.min(arr)
        self.stats[name] = [a,i]
        return (arr - i)/(a -i)

    def save(self, directory):
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
            with open(f"{folder}/best-loss.txt", "w") as f:
                f.write(str(self.loss))
                f.write("\n" + str(name))
            print(f"Saved to new folder {folder}")
        else:
            with open(f"{folder}/best-loss.txt", "r") as f:
                t = float(f.readlines()[0].strip())
            torch.save(self.best, f"{folder}/{name}.pt")
            if t > self.loss:
                with open(f"{folder}/best-loss.txt", "w") as f:
                    f.write(f"{str(self.loss)}\n{name}")
    
    def train_model(self, epochs, learningRate, data, l2_lambda=0.0):
        criterion = torch.nn.MSELoss() 
        optimizer = optim.Adam(self.parameters(), lr=learningRate, weight_decay=l2_lambda)
        print("Training")
        stats_dict = df_tensor_convert(data)
        y = stats_dict[:,0]
        x = stats_dict[:,1:]
        for epoch in range(int(epochs)):
            self.train()
            optimizer.zero_grad()
            inputs = Variable(x)
            labels = Variable(y)
            outputs = self.forward(inputs).reshape(-1)
            print(outputs)
            if (epoch + 1 %10 ==0):
                learningRate /= 2
            # get loss for the predicted output
            loss = criterion(outputs, labels)
            if torch.isnan(loss):
                raise ValueError("NAN loss")
            # get gradients w.r.t to parameters
            if self.loss > loss.item():
                print("Updated")
                self.loss = loss.item()
                self.best = deepcopy(self.state_dict())
            loss.backward()
            optimizer.step()
            print(f'epoch {epoch + 1}, loss {loss.item()}')
        print(f'Minimum loss {self.loss}')
    
    def data_fetch(self, player_year:str, mode:str):
       first, last, year = player_year.split(" ")        
       link = f"http://localhost:8080/{mode}?Name={first}-{last}&Season={year}"
       list_response = requests.get(link).json()
       if list_response is None:
           raise SearchError(f"Could not find player {first} {last}. Check for spelling and that the model is for pitching or batting\n{link}")
       keys = {y : x for x,y  in list(enumerate(self.stats))}
       valu = {x:list(y.values())[0] for x,y in list_response[0].items() if x in self.stats[:-1] and y['Valid']}
       tensor = Variable(torch.Tensor([i for _, i  in sorted(list(valu.items()), key= lambda x: keys[x[0]])]))
       return tensor
   
    
    
    def __str__(self):
        return f"Baseball model with {self.dims - 1} input dimension"

    
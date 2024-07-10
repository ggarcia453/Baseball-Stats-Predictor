import torch, numpy, pandas, os, uuid
from torch.autograd import Variable
import matplotlib.pyplot as plt
from player_stats import df_tensor_convert, grabid


class baseball_model(torch.nn.Module):
    def __init__(self, args):
        super(baseball_model, self).__init__()
        inputDim = len(args.input_args)-1
        self.linear1 = torch.nn.Linear(inputDim, 2*inputDim)
        self.linear2 = torch.nn.Linear(2*inputDim, 4*inputDim)
        self.linear3 = torch.nn.Linear(4*inputDim, 2*inputDim)
        self.linear4 = torch.nn.Linear(2*inputDim, inputDim)
        self.output = torch.nn.Linear(inputDim, 1)
        self.dims = inputDim + 1
        self.stats = args.input_args
        self.loss = -1
        self.best = None
        
    def forward(self, x):
        out = self.linear4(self.linear3(self.linear2(self.linear1(x))))
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
            # if t > self.loss:
            #     torch.save(self.best, f"{folder}/best.pt")
            #     with open(f"{folder}/best-loss.txt", "w") as f:
            #         f.write(str(self.loss))
            #     print(f"Model saved to {folder} (Overwriting)")
            # else:
            #     print("Model does not outperform best perfroming previous. Not saved")
    
    def train(self, epochs, learningRate, output, data):
        print("Training")
        stats_dict = df_tensor_convert(data)
        y = stats_dict[:,0]
        x = stats_dict[:,1:]
        for epoch in range(int(epochs)):
            inputs = Variable(x)
            labels = Variable(y)
            outputs = self.forward(inputs).reshape(-1)
            print(outputs)
            criterion = torch.nn.MSELoss() 
            optimizer = torch.optim.SGD(self.parameters(), lr=learningRate)
            if (epoch + 1 %10 ==0):
                learningRate /= 2
            # get loss for the predicted output
            loss = criterion(outputs, labels)
            if torch.isnan(loss):
                raise ValueError("NAN loss")
            # get gradients w.r.t to parameters
            if self.loss == -1:
                self.loss = loss.item()
                self.best = self.state_dict()
            elif self.loss > loss.item():
                self.loss = loss.item()
                self.best = self.state_dict()
            loss.backward()
            # update parameters
            optimizer.step()
            print(f'epoch {epoch + 1}, loss {loss.item()}')
        print(f'Minimum loss {self.loss}')
    
    def predict(self, player_year):
        ls = player_year.split("_")
        id = grabid(ls[:2]).key_mlbam[0]
        print(id)
        
    
    def __str__(self):
        return f"Baseball model with {self.dims - 1} input dimension"

    
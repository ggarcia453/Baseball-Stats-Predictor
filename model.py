import torch, numpy, pandas
from torch.autograd import Variable
from player_stats import df_tensor_convert


class baseball_model(torch.nn.Module):
    def __init__(self, inputDim ):
        super(baseball_model, self).__init__()
        self.linear1 = torch.nn.Linear(inputDim, 2*inputDim)
        self.linear2 = torch.nn.Linear(2*inputDim, 2*inputDim)
        self.linear3 = torch.nn.Linear(2*inputDim, 2*inputDim)
        self.linear4 = torch.nn.Linear(2*inputDim, inputDim)
        self.output = torch.nn.Linear(inputDim, 1)
        self.dims = inputDim + 1
        self.stats = {}
        
    def forward(self, x):
        out = self.linear4(self.linear3(self.linear2(self.linear1(x))))
        out = self.output(out)
        return out
    
    def normalize(self, arr, name):
        a,i = torch.max(arr), torch.min(arr)
        self.stats[name] = [a,i]
        return (arr - i)/(a -i)

    def save():
        torch.save(model.state_dict(), "model")
    

    def train(self, epochs, learningRate, data):
        print("Training")
        stats_dict = df_tensor_convert(data)
        stats_dict = {i: self.normalize(j,i) for i,j in stats_dict.items()}
        y = stats_dict['WAR']
        del stats_dict['WAR']
        x = torch.stack(tuple(list(stats_dict.values())),dim=1)
        for epoch in range(int(epochs)):
            inputs = Variable(x)
            labels = Variable(y)
            outputs = self.forward(inputs)
            criterion = torch.nn.MSELoss() 
            optimizer = torch.optim.SGD(self.parameters(), lr=learningRate)
            if (epoch + 1 %10 ==0):
                learningRate /= 2
            # get loss for the predicted output
            loss = criterion(outputs, labels)
            # get gradients w.r.t to parameters
            loss.backward()
            # update parameters
            optimizer.step()
            print(f'epoch {epoch + 1}, loss {loss.item()}')
        # print(self.denormalize(outputs, 'WAR'))
    
    def eval(self, *inputs):
        pass
    
    def __str__(self):
        return f"Baseball model with {self.dims - 1} input dimension"

        

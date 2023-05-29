

import torch
import torch.nn as nn
import torch.nn as nn
import os
from torchvision import transforms
from PIL import Image
from torch.autograd import Variable
from torch.nn import Linear, ReLU, CrossEntropyLoss, Sequential, Conv2d, MaxPool2d, Module, Softmax, BatchNorm2d, Dropout
from torch.optim import Adam, SGD
import torch.nn as nn
import torch.nn.functional as F
from django.conf import settings



class SimpleCNN(nn.Module):
    def __init__(self):
        # ancestor constructor call
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=2)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=2)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=2)
        self.conv4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=2)
        self.conv5 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=2)
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(128)
        self.bn4 = nn.BatchNorm2d(256)
        self.bn5 = nn.BatchNorm2d(512)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.avg = nn.AvgPool2d(8)
        self.fc = nn.Linear(512 * 1 * 1, 4) # !!!
    def forward(self, x):
        x = self.pool(F.leaky_relu(self.bn1(self.conv1(x)))) # first convolutional layer then batchnorm, then activation then pooling layer.
        x = self.pool(F.leaky_relu(self.bn2(self.conv2(x))))
        x = self.pool(F.leaky_relu(self.bn3(self.conv3(x))))
        x = self.pool(F.leaky_relu(self.bn4(self.conv4(x))))
        x = self.pool(F.leaky_relu(self.bn5(self.conv5(x))))
        x = self.avg(x)
        #print(x.shape) # lifehack to find out the correct dimension for the Linear Layer
        x = x.view(-1, 512 * 1 * 1) # !!!
        x = self.fc(x)
        return x
    
model=SimpleCNN()

# Predict function definition
def predict_image(path):
    
    #Loading Model
    checkpoint = torch.load(os.path.join(settings.BASE_DIR,'Classification task/model.ckpt'))
    # checkpoint = torch.load('model.ckpt')
    # Load the parameters into the model
    model.load_state_dict(checkpoint)
    # Set the model in evaluation mode
    model.eval()
    
    transform = transforms.Compose([transforms.Resize(225),
                                transforms.Grayscale(num_output_channels=1),
                                 transforms.CenterCrop(224), transforms.ToTensor()])
    label_map={0:'Covid-19',1:'NORMAL', 2:'PNEUMONIA',3:'TUBERCULOSIS'}
    
    # Define the transformations to be applied on the input image

    image = Image.open(path)
    image_tensor = transform(image).unsqueeze(0)

    # Pass the image through the model
    output = model(image_tensor)

    # Get the class label with the highest probability.
    _, prediction = torch.max(output.data, 1)
    
    label_name=label_map[prediction.item()]
    print("Predicted class label:", label_name)
    image=""

    return label_name
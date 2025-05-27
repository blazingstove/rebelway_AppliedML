import os
import sys
import hou
import math
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from PIL import Image
import pickle

hip_dir = os.path.dirname(hou.hipFile.path())
sys.path.append(os.path.join(hip_dir))

# FashionMNIST mapping dict()

mp_fashion = {0:"T-shirt/Top",
              1:"Trouser",
              2:"Pullover",
              3:"Dress",
              4:"Coat",
              5:"Sandal",
              6:"Shirt",
              7:"Sneaker",
              8:"Bag",
              9:"Ankle Boot"
              }

FASHIONMNIST_PATH = os.path.join(hip_dir, 'mnist_fashion_model.pth')

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} device')


# Define Neural Network training model class

class Net(nn.Module):
  
  def __init__(self):
    super().__init__()
    self.flatten = nn.Flatten()
    self.linear_relu_stack = nn.Sequential(
        nn.Linear(28*28, 512),
        nn.ReLU(),
        nn.Linear(512,512),
        nn.ReLU(),
        nn.Linear(512,10),
    )

  def forward(self, x):
    x = self.flatten(x)
    logits = self.linear_relu_stack(x)
    return logits

def identify_image(image=None, model_path=FASHIONMNIST_PATH):
    """
    Classify the specified image

        kArgs:
            image (PIL.Image): optional PIL.Image object to evaluate. If nothing is specified
                           the image specified by the "image_path" parameter will be loaded
                           and classified.

            model_path (string) : Path to trained model, default is FASHIONMNIST_PATH

        Returns:
            (int) : index classification based on loaded model
    
    """

    if not os.path.exists(model_path):
       print('Aborting...Invalid model path provided')
       return

    # Set transformer to conform the input image to
    # the format of the model's training data

    transform = transforms.Compose([ 
        transforms.ToTensor(), 
        transforms.Resize((28, 28)),
        ])
    
    # If no image was specified, load the image path 

    if image is None:
        
        image_path = hou.pwd().parm('image_path').eval()
        
        if not os.path.exists(image_path):
            print('Aborting...Invalid image path provided')
            return
        
        image = Image.open(image_path).convert("L")
    
    # Transform the image and send it to the device

    image = transform(image).to(device)
    
    # Create a new NN module, send it to the device
     
    model = Net().to(device)
    
    # Load up the trained model weights

    model.load_state_dict(torch.load(model_path))
    
    # Set the model to evaluation mode

    model.eval()
    
    # Infer the classification of the input image
    # using the model
    
    with torch.inference_mode():
        output = model(image)
        prediction = torch.argmax(output).item()
        
        print(f"Predicted: {mp_fashion[prediction]}")

        return prediction
    
def identify_drawing():
    """
    Load the "pixels" of the drawing grid into memory, turn them into an Image.PIL
    object and then call 'identify_image()' to use the trained model to classify the image

    """

    # Get the primitive data the connected SOP node 

    node = hou.pwd()
    input_nodes = node.inputs()
    geo = input_nodes[0].geometry()
    prims = geo.prims()
    
    # Iterate over the grid rows and columns sampling each
    # primitive's color attribute
    
    grid_matrix = []
    num_rows = num_cols = int(math.sqrt(len(prims)))
    
    for row in range(num_rows):
        new_row = []
        for col in range(num_cols):
            prim_index = row * num_cols + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")[0]
            new_row.append(color)
        grid_matrix.append(new_row)

    # Convert the floating point grid data to
    # 0-255 RGB color and then pass it PIL.Image
    # to generate a new Image() object 

    np_matrix = np.array(grid_matrix) * 255
    np_matrix = np_matrix.astype(np.uint8)
    image = Image.fromarray(np_matrix, mode='L')
    
    # Submit the in-memory image for classification

    identify_image(image=image)
    
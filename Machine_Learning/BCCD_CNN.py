datasetpath = "/home/jim/Downloads/dataset2-master"

import os
for dirname, _, filenames in os.walk(datasetpath):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms


# Load datasets
train_dataset = torchvision.datasets.ImageFolder(
    root=datasetpath+'/images/TRAIN',
    transform=transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
    ])
)

test_dataset = torchvision.datasets.ImageFolder(
    root=datasetpath+'/images/TEST',
    transform=transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225]) #typical form from imagenet
    ])
)

batch_size = 128
train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

class CustomCNN(nn.Module):
    def __init__(self):
        super(CustomCNN, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 4, kernel_size=3, stride=(2, 2), padding=1)
        self.conv2 = nn.Conv2d(4 , 8, kernel_size=3, stride=(2, 2), padding=1)
        self.conv3 = nn.Conv2d(8, 16, kernel_size=3, stride=(2, 2), padding=1)

        # # Batch normalization layers
        self.batch_norm1 = nn.BatchNorm2d(4)
        self.batch_norm2 = nn.BatchNorm2d(8)
        self.batch_norm3 = nn.BatchNorm2d(16)

        # Max pooling layers
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)

        # Dropout layers
        self.dropout = nn.Dropout(0.2)

        # Fully connected layers
        self.fc1 = nn.Linear(16 * 4 * 4, 32)
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 8)
        self.fc4 = nn.Linear(8, 4)  # Output layer

    def forward(self, x):
        # Convolutional layers with activation and normalization
        x = self.pool(F.relu(self.batch_norm1(self.conv1(x))))
        x = self.pool(F.relu(self.batch_norm2(self.conv2(x))))
        x = self.pool(F.relu(self.batch_norm3(self.conv3(x))))

        # Flattening step
        x = x.view(-1, 16 * 4 * 4)

        # Fully connected layers with dropout
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = F.relu(self.fc3(x))
        x = self.dropout(x)
        x = F.softmax(self.fc4(x),dim=1)  # Output layer

        return x

model = CustomCNN()
print(model)

# Initialize the model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CustomCNN().to(device)

# Define the loss function and the optimizer
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())

num_epochs = 200 
# Test accuracy: 0.8098
# Test F1 score: 0.8146
# Test AUC score: 0.8999

losses = []

# Train
for epoch in range(num_epochs):
    model.train()
    for inputs, labels in train_dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        logits = model(inputs)
        loss = loss_fn(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    losses.append(loss.item())
    print(f'Loss at epoch {epoch+1}: {loss.item():.4f}')

import matplotlib.pyplot as plt

# Plot the loss values
plt.plot(losses)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()

from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import numpy as np

model.eval()
true_labels = []
pred = []

# Test
with torch.no_grad():
    for inputs, labels in test_dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        logits = model(inputs)
        probs = torch.softmax(logits, dim=1)  # calculate probabilities

        true_labels.extend(labels.tolist())
        pred.extend(probs.tolist())

true_labels = np.array(true_labels)
pred = np.array(pred)

acc = accuracy_score(true_labels, np.argmax(pred, axis=1))
f1 = f1_score(true_labels, np.argmax(pred, axis=1), average='macro')
auc = roc_auc_score(true_labels, pred, multi_class='ovo')

print(f'Test accuracy: {acc:.4f}')
print(f'Test F1 score: {f1:.4f}')
print(f'Test AUC score: {auc:.4f}')
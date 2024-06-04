import numpy as np
import numpy.typing as npt
import torch

from binside_common.processing import FileType


class Model(torch.nn.Module):
    def __init__(self, classes_count: int) -> None:
        super().__init__()

        self.conv1 = torch.nn.Sequential(
            # first conv layer
            torch.nn.Conv2d(1, 16, 3),
            torch.nn.ReLU(True),
            torch.nn.BatchNorm2d(16))
        self.conv2 = torch.nn.Sequential(
            # second conv layer
            torch.nn.Conv2d(16, 32, 5),
            torch.nn.ReLU(True),
            torch.nn.BatchNorm2d(32),
            torch.nn.MaxPool2d(2),
            torch.nn.Dropout2d(0.25))
        # self.conv3 = torch.nn.Sequential(
        #     # # third conv layer
        #     torch.nn.Conv2d(512, 1024, 3),
        #     torch.nn.ReLU(True),
        #     torch.nn.BatchNorm2d(1024),
        #     torch.nn.Dropout2d(0.25))

        self.flatten = torch.nn.Flatten()

        self.lin1 = torch.nn.Sequential(
            # first linear layer
            torch.nn.Linear(32 * 125 * 125, 512),
            torch.nn.ReLU(True),
            torch.nn.BatchNorm1d(512),
            torch.nn.Dropout(0.5))
        self.lin2 = torch.nn.Sequential(
            # second linear layer
            torch.nn.Linear(512, 64),
            torch.nn.ReLU(True),
            torch.nn.BatchNorm1d(64),
            torch.nn.Dropout(0.5))
        self.lin3 = torch.nn.Sequential(
            # classification layer
            torch.nn.Linear(64, classes_count),
            torch.nn.Softmax(1))

        # self.conv1 = torch.nn.Conv2d(1, 6, 5)
        # self.pool = torch.nn.MaxPool2d(2, 2)
        # self.conv2 = torch.nn.Conv2d(6, 16, 5)
        # self.conv3 = torch.nn.Conv2d(16, 8, 2)
        # self.fc1 = torch.nn.Linear(8*60*60, 1024)
        # self.fc2 = torch.nn.Linear(1024, 120)
        # self.fc3 = torch.nn.Linear(120, 40)
        # self.fc4 = torch.nn.Linear(40, classes_count)

        # # self.features = torch.nn.Sequential(
        # #     torch.nn.Conv2d(1, 32, kernel_size=12, bias=False),
        # #     torch.nn.ReLU(inplace=True),
        # #     torch.nn.Conv2d(32, 64, kernel_size=8),
        # #     torch.nn.ReLU(inplace=True),
        # #     torch.nn.Conv2d(64, 64, kernel_size=4))
        # # self.classifier = torch.nn.Sequential(
        # #     torch.nn.Dropout(),
        # #     torch.nn.Linear(64 * 64, 2048),
        # #     torch.nn.ReLU(inplace=True),
        # #     torch.nn.Dropout(),
        # #     torch.nn.Linear(2048, 128),
        # #     torch.nn.ReLU(inplace=True),
        # #     torch.nn.Linear(128, classes_count))

    def forward(self, x: object) -> object:
        x = self.conv1.forward(x)
        x = self.conv2.forward(x)
        x = self.flatten.forward(x)
        x = self.lin1.forward(x)
        x = self.lin2.forward(x)
        return self.lin3.forward(x)

        x = self.pool(torch.nn.functional.relu(self.conv1(x)))
        x = self.pool(torch.nn.functional.relu(self.conv2(x)))
        x = torch.nn.functional.relu(self.conv3(x))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = torch.nn.functional.relu(self.fc3(x))
        x = self.fc4(x)
        return x

def get_training_device() -> str:
    if torch.cuda.is_available():
        return 'cuda'
    elif torch.is_vulkan_available():
        return 'vulkan'
    elif torch.backends.mps.is_available():
        return 'mps'
    elif torch.backends.openmp.is_available():
        return 'openmp'
    else:
        return 'cpu'

def load_model(filepath: str) -> Model:
    classes_count = len(FileType.__members__)
    model = Model(classes_count)

    with open(filepath, 'rb') as f:
        model_state = torch.load(f)

    model.load_state_dict(model_state)

    return model

def classify_memory_map(model: Model, memory_map: npt.NDArray[np.float32]) -> dict[str, float]:
    model.eval()

    tensor = torch.tensor(memory_map).unsqueeze_(0).unsqueeze_(0)
    result = model(tensor)
    certainities = result.data.tolist()[0]
    predictions = {k: v for k, v in zip(FileType.__members__.keys(), certainities)}
    return predictions

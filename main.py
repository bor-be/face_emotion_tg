import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
num_classes = 7
weights_path = "weights_epoch_26.pth"


class ResNet34Pretrained(nn.Module):
    def __init__(self, num_classes=7):
        super().__init__()

        self.model = models.resnet34(weights=models.ResNet34_Weights.IMAGENET1K_V1)

        old_weight = self.model.conv1.weight.data
        self.model.conv1 = nn.Conv2d(
            1, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.model.conv1.weight.data = old_weight.mean(dim=1, keepdim=True)

        self.model.maxpool = nn.Identity()

        in_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Dropout(0.5), nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.model(x)


model = ResNet34Pretrained(num_classes=num_classes).to(device)
model.load_state_dict(torch.load(weights_path, map_location=device))
model.eval()


transform = transforms.Compose(
    [
        transforms.Grayscale(),
        transforms.Resize((48, 48)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),
    ]
)


def predict_image(image: Image.Image):
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image)
        probs = torch.softmax(output, dim=1)
        pred = torch.argmax(probs, dim=1).item()
        confidence = probs[0, pred].item()
    return pred, confidence

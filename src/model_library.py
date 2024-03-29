from abc import ABC, abstractmethod
import torchxrayvision as xrv
import torchvision
from torchvision.transforms.functional import normalize

class AbstractModelLibrary:
    def __init__(self):
        self.CHOICES = []
        self.LABELS = []
        self.TARGET_LAYER = None

    @abstractmethod
    def get_model(self, choice: str):
        pass

    @abstractmethod
    def preprocess(self, img):
        pass

class XRVModelLibrary(AbstractModelLibrary):
    def __init__(self):
        super().__init__()
        self.CHOICES = [
            "densenet121-res224-all",
            "densenet121-res224-rsna",
            "densenet121-res224-nih",
            "densenet121-res224-pc",
            "densenet121-res224-chex",
            "densenet121-res224-mimic_nb",
            "densenet121-res224-mimic_ch",
        ]

    def get_model(self, choice: str):
        model = xrv.models.DenseNet(weights=choice)
        self.LABELS = model.targets
        self.TARGET_LAYER = model.features[10][-1][5]
        return model.eval()

    def preprocess(self, img):
        transform = torchvision.transforms.Compose([
                torchvision.transforms.Grayscale(num_output_channels=1),
                torchvision.transforms.CenterCrop(max(img.shape)),
                torchvision.transforms.Resize((224,224)),
                ])
        transformed_output = transform(img)

        img_min = transformed_output.min()
        img_max = transformed_output.max()

        rescaled_output = 2048*(transformed_output-img_min)/(img_max-img_min) - 1024
        return transformed_output, rescaled_output

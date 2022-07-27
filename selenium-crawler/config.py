import os
from pathlib import Path

realpath = Path(os.path.realpath(__file__)).parent
model_path = os.path.join(realpath, 'trained_model')

class MTCNNConfig:
    MODEL_PATH = os.path.join(model_path, 'mtcnn_weights.npy')
    STEPS_THRESHOLD = [0.8, 0.9, 0.99]
import numpy as np
import pickle
import codecs

# https://stackoverflow.com/questions/30469575/how-to-pickle-and-unpickle-to-portable-string-in-python-3


def serialize(frame: np.ndarray) -> str:
    return codecs.encode(pickle.dumps(frame), "base64").decode()


def parse(raw_frame: str) -> np.ndarray:
    return pickle.loads(codecs.decode(raw_frame.encode(), "base64"))

import pickle
from subprocess import Popen
import sys


def save_pickles(filename, data):
    with open(filename,'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickles(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def execute(commands):
    with Popen(commands, shell=True) as process:
        try:
            process.communicate()
        except Exception as e:
            process.kill()
            raise e

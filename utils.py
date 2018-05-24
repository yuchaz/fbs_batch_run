import pickle

def save_pickles(filename, data):
    with open(filename,'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickles(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

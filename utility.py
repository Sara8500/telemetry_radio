import pickle


def pickle_result(data, filename):
    f = open(filename, 'wb')
    pickle.dump(data, f)


def unpickle_result(filename):
    with open(filename, 'rb') as f:
        results = pickle.load(f)
        return results
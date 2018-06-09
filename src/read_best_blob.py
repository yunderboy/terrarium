import pickle

if __name__ == '__main__':
    with open(r'best_blob.pkl', 'rb') as input_file:
        print(pickle.load(input_file))

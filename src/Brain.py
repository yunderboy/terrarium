import numpy as np

np.random.seed(1)

class NeuralNetwork(object):
    def __init__(self, input, hidden, output):
        """
        :param input: number of input neurons
        :param hidden: number of hidden neurons
        :param output: number of output neurons
        """

        self.input = input + 1 # add 1 for bias node
        self.hidden = hidden
        self.output = output
        # set up array of 1s for activations
        self.ai = [1.0] * self.input
        self.ah = [1.0] * self.hidden
        self.ao = [1.0] * self.output
        # create randomized weights
        self.wi = np.random.randn(self.input, self.hidden)
        self.wo = np.random.randn(self.hidden, self.output)
        # create arrays of 0 for changes
        self.ci = np.zeros((self.input, self.hidden))
        self.co = np.zeros((self.hidden, self.output))

    def feed_forward(self, inputs):
        if len(inputs) != self.input-1:
            raise ValueError('Wrong number of inputs you silly goose!')
            # input activations
        for i in range(self.input -1): # -1 is to avoid the bias
            self.ai[i] = inputs[i]
            # hidden activations
        for j in range(self.hidden):
            sum = 0.0
            for i in range(self.input):
                sum += self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)
            # output activations
        for k in range(self.output):
            sum = 0.0
            for j in range(self.hidden):
                sum += self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)
        return self.ao[:]


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


if __name__ == '__main__':
    nn = NeuralNetwork(3, 4, 2)
    print(nn)
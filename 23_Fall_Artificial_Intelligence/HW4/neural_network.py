import numpy as np


def load_data_small():
    """ Load small training and validation dataset

        Returns a tuple of length 4 with the following objects:
        X_train: An N_train-x-M ndarray containing the training data (N_train examples, M features each)
        y_train: An N_train-x-1 ndarray contraining the labels
        X_val: An N_val-x-M ndarray containing the training data (N_val examples, M features each)
        y_val: An N_val-x-1 ndarray contraining the labels
    """
    train_all = np.loadtxt('data/smallTrain.csv', dtype=int, delimiter=',')
    valid_all = np.loadtxt('data/smallValidation.csv', dtype=int, delimiter=',')

    X_train = train_all[:, 1:]
    y_train = train_all[:, 0]
    X_val = valid_all[:, 1:]
    y_val = valid_all[:, 0]

    return (X_train, y_train, X_val, y_val)


def load_data_medium():
    """ Load medium training and validation dataset

        Returns a tuple of length 4 with the following objects:
        X_train: An N_train-x-M ndarray containing the training data (N_train examples, M features each)
        y_train: An N_train-x-1 ndarray contraining the labels
        X_val: An N_val-x-M ndarray containing the training data (N_val examples, M features each)
        y_val: An N_val-x-1 ndarray contraining the labels
    """
    train_all = np.loadtxt('data/mediumTrain.csv', dtype=int, delimiter=',')
    valid_all = np.loadtxt('data/mediumValidation.csv', dtype=int, delimiter=',')

    X_train = train_all[:, 1:]
    y_train = train_all[:, 0]
    X_val = valid_all[:, 1:]
    y_val = valid_all[:, 0]

    return (X_train, y_train, X_val, y_val)


def load_data_large():
    """ Load large training and validation dataset

        Returns a tuple of length 4 with the following objects:
        X_train: An N_train-x-M ndarray containing the training data (N_train examples, M features each)
        y_train: An N_train-x-1 ndarray contraining the labels
        X_val: An N_val-x-M ndarray containing the training data (N_val examples, M features each)
        y_val: An N_val-x-1 ndarray contraining the labels
    """
    train_all = np.loadtxt('data/largeTrain.csv', dtype=int, delimiter=',')
    valid_all = np.loadtxt('data/largeValidation.csv', dtype=int, delimiter=',')

    X_train = train_all[:, 1:]
    y_train = train_all[:, 0]
    X_val = valid_all[:, 1:]
    y_val = valid_all[:, 0]

    return (X_train, y_train, X_val, y_val)


def linearForward(input, p):
    """
    :param input: input vector (column vector) WITH bias feature added
    :param p: parameter matrix (alpha/beta) WITH bias parameter added
    :return: output vector
    """

    output = np.dot(p, input)
    return output


def sigmoidForward(a):
    """
    :param a: input vector WITH bias feature added
    """

    try:    # avoid overflow
        sigmoid_a = 1 / (1 + np.exp(-a))
    except:
        return np.zeros(a.shape)
    
    return sigmoid_a


def softmaxForward(b):
    """
    :param b: input vector WITH bias feature added
    """

    exp_b = np.exp(b - np.max(b))   # avoid overflow
    if np.sum(exp_b) == 0:  # avoid divide by 0
        return np.zeros(exp_b.shape)
    softmax_b = exp_b / np.sum(exp_b)
    return softmax_b


def crossEntropyForward(hot_y, y_hat):
    """
    :param hot_y: 1-hot vector for true label
    :param y_hat: vector of probabilistic distribution for predicted label
    :return: float
    """
    
    cross_entropy = -np.sum(hot_y * np.log(y_hat + 0.0000000001))   # avoid 0 in log
    return cross_entropy


def NNForward(x, y, alpha, beta):
    """
    :param x: input data (column vector) WITH bias feature added
    :param y: input (true) labels
    :param alpha: alpha WITH bias parameter added
    :param beta: alpha WITH bias parameter added
    :return: all intermediate quantities x, a, z, b, y, J #refer to writeup for details
    TIP: Check on your dimensions. Did you make sure all bias features are added?
    """

    a = linearForward(x, alpha)
    z = sigmoidForward(a)

    z = np.insert(z, 0, 1)  # add bias feature 

    b = linearForward(z, beta)
    y_hat = softmaxForward(b)

    hot_y = np.zeros(len(y_hat))
    hot_y[y] = 1

    J = crossEntropyForward(hot_y, y_hat)
    return x, a, z, b, y_hat, J


def softmaxBackward(hot_y, y_hat):
    """
    :param hot_y: 1-hot vector for true label
    :param y_hat: vector of probabilistic distribution for predicted label
    """

    softmax_gradient = y_hat - hot_y
    return softmax_gradient


def linearBackward(prev, p, grad_curr):
    """
    :param prev: previous layer WITH bias feature
    :param p: parameter matrix (alpha/beta) WITH bias parameter
    :param grad_curr: gradients for current layer
    :return:
        - grad_param: gradients for parameter matrix (alpha/beta)
        - grad_prevl: gradients for previous layer
    TIP: Check your dimensions.
    """

    grad_param = np.outer(grad_curr, prev)
    grad_prevl = np.dot(p.T, grad_curr)
    return grad_param, grad_prevl


def sigmoidBackward(curr, grad_curr):
    """
    :param curr: current layer WITH bias feature
    :param grad_curr: gradients for current layer
    :return: grad_prevl: gradients for previous layer
    TIP: Check your dimensions
    """

    sigmoid_grad = (1 - curr) * curr
    grad_prevl = grad_curr * sigmoid_grad
    return grad_prevl


def NNBackward(x, y, alpha, beta, z, y_hat):
    """
    :param x: input data (column vector) WITH bias feature added
    :param y: input (true) labels
    :param alpha: alpha WITH bias parameter added
    :param beta: alpha WITH bias parameter added
    :param z: z as per writeup
    :param y_hat: vector of probabilistic distribution for predicted label
    :return:
        - grad_alpha: gradients for alpha
        - grad_beta: gradients for beta
        - g_b: gradients for layer b (softmaxBackward)
        - g_z: gradients for layer z (linearBackward)
        - g_a: gradients for layer a (sigmoidBackward)
    """

    hot_y = np.zeros(len(y_hat))
    hot_y[y] = 1

    g_b = softmaxBackward(hot_y, y_hat)
    grad_beta, g_z = linearBackward(z, beta, g_b)
    g_a = sigmoidBackward(z, g_z)
    grad_alpha, grad_prevl = linearBackward(x, alpha, g_a[1:])

    return grad_alpha, grad_beta, g_b, g_z, g_a



def SGD(tr_x, tr_y, valid_x, valid_y, hidden_units, num_epoch, init_flag, learning_rate):
    """
    :param tr_x: Training data input (size N_train x M)
    :param tr_y: Training labels (size N_train x 1)
    :param tst_x: Validation data input (size N_valid x M)
    :param tst_y: Validation labels (size N_valid x 1)
    :param hidden_units: Number of hidden units
    :param num_epoch: Number of epochs
    :param init_flag:
        - True: Initialize weights to random values in Uniform[-0.1, 0.1], bias to 0
        - False: Initialize weights and bias to 0
    :param learning_rate: Learning rate
    :return:
        - alpha weights
        - beta weights
        - train_entropy (length num_epochs): mean cross-entropy loss for training data for each epoch
        - valid_entropy (length num_epochs): mean cross-entropy loss for validation data for each epoch
    """
    
    input_size = tr_x.shape[1]
    output_size = len(np.unique(tr_y))

    # definition alpha, beta
    alpha = None
    beta = None

    # initialize parameters alpha, beta
    if init_flag:
        alpha = np.random.uniform(-0.1, 0.1, size=(hidden_units, input_size + 1))
        beta = np.random.uniform(-0.1, 0.1, size=(output_size, hidden_units + 1))
    else:
        alpha = np.zeros((hidden_units, input_size + 1))
        beta = np.zeros((output_size, hidden_units + 1))

    train_entropy = []
    valid_entropy = []
    #print("alpha", alpha,flush=True)
    #print("beta", beta,flush=True)

    for epoch in range(num_epoch):
        for in_x, in_y in zip(tr_x, tr_y):
            in_x.reshape(1, -1)
            in_x = np.insert(in_x, 0, 1)

            # compute neural network layers
            x, a, z, b, y_hat, J = NNForward(in_x, in_y, alpha, beta)

            # compute gradients via backprop
            grad_alpha, grad_beta, g_b, g_z, g_a = NNBackward(x, in_y, alpha, beta, z, y_hat)

            # update parameters
            alpha -= learning_rate * grad_alpha
            beta -= learning_rate * grad_beta

        train_entropy_epoch = 0
        valid_entropy_epoch = 0

        # Store training mean cross entropy
        for in_x, in_y in zip(tr_x, tr_y):
            in_x.reshape(1, -1)
            in_x = np.insert(in_x, 0, 1)

            x, a, z, b, y_hat, J = NNForward(in_x, in_y, alpha, beta)

            train_entropy_epoch += J

        # Store validation mean cross entropy
        for in_x, in_y in zip(valid_x, valid_y):
            in_x.reshape(1, -1)
            in_x = np.insert(in_x, 0, 1)

            x, a, z, b, y_hat, J = NNForward(in_x, in_y, alpha, beta)

            valid_entropy_epoch += J

        mean_train_entropy_epoch = train_entropy_epoch / len(tr_y)
        mean_valid_entropy_epoch = valid_entropy_epoch / len(valid_y)

        train_entropy.append(mean_train_entropy_epoch)
        valid_entropy.append(mean_valid_entropy_epoch)

    return alpha, beta, train_entropy, valid_entropy


def prediction(tr_x, tr_y, valid_x, valid_y, tr_alpha, tr_beta):
    """
    :param tr_x: Training data input (size N_train x M)
    :param tr_y: Training labels (size N_train x 1)
    :param valid_x: Validation data input (size N_valid x M)
    :param valid_y: Validation labels (size N-valid x 1)
    :param tr_alpha: Alpha weights WITH bias
    :param tr_beta: Beta weights WITH bias
    :return:
        - train_error: training error rate (float)
        - valid_error: validation error rate (float)
        - y_hat_train: predicted labels for training data
        - y_hat_valid: predicted labels for validation data
    """

    y_hat_train = []
    y_hat_valid = []

    train_error_num = 0
    valid_error_num = 0

    # prediction in train data
    for in_x, in_y in zip(tr_x, tr_y):
        in_x.reshape(1, -1)
        in_x = np.insert(in_x, 0, 1)

        x, a, z, b, y_hat, J = NNForward(in_x, in_y, tr_alpha, tr_beta)
        predicted_label = np.argmax(y_hat)

        y_hat_train.append(predicted_label)
        if predicted_label != in_y:
            train_error_num += 1

    # prediction in valid data
    for in_x, in_y in zip(valid_x, valid_y):
        in_x.reshape(1, -1)
        in_x = np.insert(in_x, 0, 1)

        x, a, z, b, y_hat, J = NNForward(in_x, in_y, tr_alpha, tr_beta)
        predicted_label = np.argmax(y_hat)

        y_hat_valid.append(predicted_label)
        if predicted_label != in_y:
            valid_error_num += 1

    train_error = train_error_num / len(tr_y)
    valid_error = valid_error_num / len(valid_y)

    return train_error, valid_error, y_hat_train, y_hat_valid

### FEEL FREE TO WRITE ANY HELPER FUNCTIONS

def train_and_valid(X_train, y_train, X_val, y_val, num_epoch, num_hidden, init_rand, learning_rate):
    """ Main function to train and validate your neural network implementation.

        X_train: Training input in N_train-x-M numpy nd array. Each value is binary, in {0,1}.
        y_train: Training labels in N_train-x-1 numpy nd array. Each value is in {0,1,...,K-1},
            where K is the number of classes.
        X_val: Validation input in N_val-x-M numpy nd array. Each value is binary, in {0,1}.
        y_val: Validation labels in N_val-x-1 numpy nd array. Each value is in {0,1,...,K-1},
            where K is the number of classes.
        num_epoch: Positive integer representing the number of epochs to train (i.e. number of
            loops through the training data).
        num_hidden: Positive integer representing the number of hidden units.
        init_flag: Boolean value of True/False
        - True: Initialize weights to random values in Uniform[-0.1, 0.1], bias to 0
        - False: Initialize weights and bias to 0
        learning_rate: Float value specifying the learning rate for SGD.

        RETURNS: a tuple of the following six objects, in order:
        loss_per_epoch_train (length num_epochs): A list of float values containing the mean cross entropy on training data after each SGD epoch
        loss_per_epoch_val (length num_epochs): A list of float values containing the mean cross entropy on validation data after each SGD epoch
        err_train: Float value containing the training error after training (equivalent to 1.0 - accuracy rate)
        err_val: Float value containing the validation error after training (equivalent to 1.0 - accuracy rate)
        y_hat_train: A list of integers representing the predicted labels for training data
        y_hat_val: A list of integers representing the predicted labels for validation data
    """
    ### YOUR CODE HERE

    loss_per_epoch_train = []
    loss_per_epoch_val = []
    err_train = None
    err_val = None
    y_hat_train = None
    y_hat_val = None

    alpha, beta, loss_per_epoch_train, loss_per_epoch_val = SGD(X_train, y_train, X_val, y_val, num_hidden, num_epoch, init_rand, learning_rate)
    err_train, err_val, y_hat_train, y_hat_val = prediction(X_train, y_train, X_val, y_val, alpha, beta)

    return (loss_per_epoch_train, loss_per_epoch_val,
            err_train, err_val, y_hat_train, y_hat_val)

# For debugging
'''
X_train, y_train, X_val, y_val = load_data_medium()
loss_per_epoch_train, loss_per_epoch_val, err_train, err_val, y_hat_train, y_hat_val = train_and_valid(X_train, y_train, X_val, y_val, 20, 64, True, 0.5)
print(loss_per_epoch_train)
print(loss_per_epoch_val)
print(err_train)
print(err_val)
print(y_hat_train)
print(y_hat_val)
#'''
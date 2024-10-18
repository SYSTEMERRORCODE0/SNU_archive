import numpy as np
import matplotlib.pyplot as plt


def load_knn_data():
    test_inputs = np.genfromtxt('knn-dataset/test_inputs.csv', delimiter=','),
    test_labels = np.genfromtxt('knn-dataset/test_labels.csv', delimiter=','),
    train_inputs = np.genfromtxt('knn-dataset/train_inputs.csv', delimiter=','),
    train_labels = np.genfromtxt('knn-dataset/train_labels.csv', delimiter=','),
    return train_inputs, train_labels, test_inputs, test_labels


'''
This function implements the KNN classifier to predict the label of a data point. 
Measure distances with the Euclidean norm (L2 norm).  
When there is a tie between two (or more) labels, break the tie by choosing any label.

Inputs:
    **x**: input data point for which we want to predict the label (numpy array of M features)
    **inputs**: matrix of data points in which neighbors will be found (numpy array of N data points x M features)
    **labels**: vector of labels associated with the data points  (numpy array of N labels)
    **k_neighbors**: # of nearest neighbors that will be used
Outputs:
    **predicted_label**: predicted label (integer)
'''   
def predict_knn(x, inputs, labels, k_neighbors):
    predicted_label = 0
    ########
    # TO DO:

    # get distance from x
    x_dist = np.linalg.norm(x - inputs, axis=1)

    # get k nearest neighbors
    x_label_dist = []
    for i in range(len(inputs)):
        x_label_dist.append([labels[i], x_dist[i]])
    k_nearest = sorted(x_label_dist, key=lambda l:l[1])[:k_neighbors]

    # get most label (smaller label if most labels are multiple)
    k_nearest_labels = []
    for i in k_nearest:
        k_nearest_labels.append(i[0])
    predicted_label = np.argmax(np.bincount(k_nearest_labels))

    ########
    return predicted_label


'''
This function evaluates the accuracy of the KNN classifier on a dataset. 
The dataset to be evaluated consists of (inputs, labels). 
The dataset used to find nearest neighbors consists of (train_inputs, train_labels).

Inputs:
   **inputs**: matrix of input data points to be evaluated (numpy array of N data points x M features)
   **labels**: vector of target labels for the inputs (numpy array of N labels)
   **train_inputs**: matrix of input data points in which neighbors will be found (numpy array of N' data points x M features)
   **train_labels**: vector of labels for the training inputs (numpy array of N' labels)
   **k_neighbors**: # of nearest neighbors to be used (integer)
Outputs:
   **accuracy**: percentage of correctly labeled data points (float)
'''
def eval_knn(inputs, labels, train_inputs, train_labels, k_neighbors):
    accuracy = 0
    ########
    # TO DO:

    # convert tuple to array
    # loaded data has some error that gives the array as the first value of tuple
    if type(inputs) is tuple:
        inputs = inputs[0]
    if type(labels) is tuple:
        labels = labels[0]
    if type(train_inputs) is tuple:
        train_inputs = train_inputs[0]
    if type(train_labels) is tuple:
        train_labels = train_labels[0]

    input_correct = 0

    # label predict from trained sets and get corrected nums
    for i in range(len(inputs)):
        label_prediction = predict_knn(inputs[i], train_inputs, train_labels, k_neighbors)
        if label_prediction == labels[i]:
            input_correct += 1

    accuracy = (input_correct / len(inputs)) * 100

    ########
    return accuracy


'''
This function performs k-fold cross validation to determine the best number of neighbors for KNN.
        
Inputs:
    **k_folds**: # of folds in cross-validation (integer)
    **hyperparameters**: list of hyperparameters where each hyperparameter is a different # of neighbors (list of integers)
    **inputs**: matrix of data points to be used when searching for neighbors (numpy array of N data points by M features)
    **labels**: vector of labels associated with the inputs (numpy array of N labels)
Outputs:
    **best_hyperparam**: best # of neighbors for KNN (integer)
    **best_accuracy**: accuracy achieved with best_hyperparam (float)
    **accuracies**: vector of accuracies for the corresponding hyperparameters (numpy array of floats)
'''
def cross_validation_knn(k_folds, hyperparameters, inputs, labels):
    best_hyperparam = 0
    best_accuracy = 0
    accuracies = np.zeros(len(hyperparameters))
    ########
    # TO DO:

    # convert tuple to array
    # loaded data has some error that gives the array as the first value of tuple
    if type(inputs) is tuple:
        inputs = inputs[0]
    if type(labels) is tuple:
        labels = labels[0]

    fold_size = len(inputs) // k_folds

    for i in hyperparameters:

        #print(i,flush=True)    # checking for running well

        accuracy = 0
        # divide inputs, labels into test/train sets, then run eval_knn for get accuracy
        for j in range(k_folds):
            test_inputs = inputs[j * fold_size : (j+1) * fold_size]
            test_labels = labels[j * fold_size : (j+1) * fold_size]

            train_inputs = np.concatenate((inputs[:j * fold_size], inputs[(j+1) * fold_size:]))
            train_labels = np.concatenate((labels[:j * fold_size], labels[(j+1) * fold_size:]))

            accuracy_fold = eval_knn(test_inputs, test_labels, train_inputs, train_labels, i) / k_folds
            accuracy += accuracy_fold

        accuracies[i-1] = accuracy
        if accuracy > best_accuracy:    # get best accuracy
            best_accuracy = accuracy
            best_hyperparam = i

    ########
    return best_hyperparam, best_accuracy, accuracies


'''
This function plots the KNN accuracies for different # of neighbors (hyperparameters) based on cross validation

Inputs:
    **accuracies**: vector of accuracies for the corresponding hyperparameters (numpy array of floats)
    **hyperparams**: list of hyperparameters where each hyperparameter is a different # of neighbors (list of integers)
'''
def plot_knn_accuracies(accuracies, hyperparams):
    plt.plot(hyperparams, accuracies)
    plt.ylabel('accuracy')
    plt.xlabel('k neighbors')
    plt.show()


def main():
    # load data
    train_inputs, train_labels, test_inputs, test_labels = load_knn_data()
    print(train_inputs)
    
    # number of neighbors to be evaluated by cross validation
    hyperparams = range(1,31)
    k_folds = 10

    # use k-fold cross validation to find the best # of neighbors for KNN
    best_k_neighbors, best_accuracy, accuracies = cross_validation_knn(k_folds, hyperparams, train_inputs, train_labels)

    # plot results
    plot_knn_accuracies(accuracies, hyperparams)
    print('best # of neighbors k: ' + str(best_k_neighbors))
    print('best cross validation accuracy: ' + str(best_accuracy))

    # evaluate with best # of neighbors
    accuracy = eval_knn(test_inputs, test_labels, train_inputs, train_labels, best_k_neighbors)
    print('test accuracy: '+ str(accuracy))


if __name__ == "__main__":
    main()
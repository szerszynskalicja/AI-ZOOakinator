import csv
import math
import numpy as np
import pandas as pd
from pprint import pprint
import sys
import time
import warnings
import Akinator

warnings.simplefilter(action='ignore', category=FutureWarning)

# Calculate the entropy of given column 'column_name'
def entropy(column_name, missing):
    uniqueValues, occurenceCount = np.unique(column_name,
                                             return_counts=True)  # array of unique values, number of occurence of each unique value
    entropy = 0

    # implementation of the entropy formula
    for i in range(len(uniqueValues)):
        if missing == 1 or missing == 0 and uniqueValues[i] != '?':
            entropy += (-occurenceCount[i] / np.sum(occurenceCount)) * np.log2(
                occurenceCount[i] / np.sum(occurenceCount))

    return entropy


# Calculate the information gain of given column
def infoGain(data, attribute_name):
    # data = The dataset for whose feature the IG should be calculated
    # attribute_name = the name of the feature for which the information gain should be calculated

    total_entropy = entropy(data["name"], 0)  # Calculate the entropy of the total dataset
    values, counts = np.unique(data[attribute_name],
                               return_counts=True)  # Calculate the values and the corresponding counts for the split attribute
    # Calculate the weighted entropy
    weighted_entropy = 0
    if '?' in values:
        for i in range(len(values)):
            if values[i] != '?':
                tmp = np.sum(counts) - counts[-1]
                if tmp == 0:
                    tmp = sys.maxsize
                weighted_entropy += (counts[i] / tmp) * entropy(
                    data.where(data[attribute_name] == values[i]).dropna()["name"], 0)
        tmp = np.sum(counts)
        if tmp == 0:
            tmp = sys.maxsize
        x = (np.sum(counts) - counts[-1]) / tmp
    else:
        for i in range(len(values)):
            tmp = np.sum(counts)
            if tmp == 0:
                tmp = sys.maxsize
            weighted_entropy += (counts[i] / tmp) * entropy(
                data.where(data[attribute_name] == values[i]).dropna()["name"], 0)
        x = 1
    # Calculate the information gain = Entropy(Decision)-Entropy(attribute)
    information_gain = x * (total_entropy - weighted_entropy)
    return information_gain


def gainRatio(data, attribute_name):
    tmp = entropy(data[attribute_name], 1)
    if math.isnan(tmp) or tmp == 0:
        tmp = sys.maxsize
    return infoGain(data, attribute_name) / tmp


# Algorithm implementation
def C45(data, originaldata, features, parent_node_class=None):
    # data = the data for which the ID3 algorithm should be run --> In the first run this equals the total dataset
    # originaldata = This is the original dataset needed to calculate the mode target feature value of the original dataset in the case the dataset delivered by the first parameter is empty
    # features = the feature space of the dataset . This is needed for the recursive call since during the tree growing processwe have to remove features from our dataset --> Splitting at each node
    # parent_node_class = This is the value or class of the mode target feature value of the parent node for a specific node. This is also needed for the recursive call.

    # Define the stopping criteria --> If one of this is satisfied, we want to return a leaf node#

    # If all target_values have the same value, return this value
    if len(np.unique(data["name"])) <= 1:
        return np.unique(data["name"])[0]

    # If the dataset is empty, return the mode target feature value in the original dataset
    elif len(data) == 0:
        return np.unique(originaldata["name"])[
            np.argmax(np.unique(originaldata["name"], return_counts=True)[1])]

    # If the feature space is empty, return the mode target feature value of the direct parent node.
    elif len(features) == 0:
        return parent_node_class

    # If none of the above holds true, grow the tree!
    else:
        # Set the default value for this node --> The mode target feature value of the current node
        parent_node_class = np.unique(data["name"])[
            np.argmax(np.unique(data['name'], return_counts=True)[1])]

        # Select the feature which best splits the dataset
        item_values = [gainRatio(data, feature) for feature in
                       features]  # Return the information gain values for the features in the dataset
        # print(item_values)

        # Calculate the best feature to split the tree (with the biggest information gain)
        best_feature_index = np.argmax(item_values)
        best_feature = features[best_feature_index]

        # Create the tree structure. The root gets the name of the feature (best_feature) with the maximum information gain in the first run
        tree = {best_feature: {}}

        # Remove the feature with the best inforamtion gain from the feature space
        features = [f for f in features if f != best_feature]

        # Grow a branch under the root node for each possible value of the root node feature
        for value in np.unique(data[best_feature]):
            # value = value
            # Split the dataset along the value of the feature with the largest information gain and therwith create sub_datasets
            sub_data = data.where(data[best_feature] == value).dropna()

            # Call the ID3 algorithm for each of those sub_datasets with the new parameters --> Here the recursion comes in!
            subtree = C45(sub_data, dataset, features, parent_node_class)

            # Add the sub tree, grown from the sub_dataset to the tree under the root node
            tree[best_feature][value] = subtree

        return (tree)


###################

attribute_names = []
attributes = csv.reader(open("zoo/attributes.csv"), delimiter=',', quoting=csv.QUOTE_MINIMAL)

for row in attributes:
    attribute_names = row
    dataset = pd.read_csv('zoo/zoo._polskie.csv', names=row)

start_time = time.time()
tree = C45(dataset, dataset, dataset.columns[:-1])
end_time = time.time() - start_time
pprint(tree)
print("Czas budowania drzewa: " + str(end_time) + " [s]")
Akinator.akinator(tree)

"""
* Name: Yolanda Meng
* Date: 2025.2.20
* CSE 160, Autumn 2024
* Homework 4
* Description:
* Collaboration:
"""

from utils import load_centroids, read_data
from kmeans import get_closest_centroid  # noqa: F401


# ----------------------------------------------------------
# PROBLEMS FOR STUDENTS
def assign_labels(list_of_points, labels, centroids_dict):
    """
    Assign all data points to the closest centroids and keep track of their
    labels. The i-th point in "data" corresponds to the i-th label in "labels".

    Arguments:
        list_of_points: a list of lists representing all data points
        labels: a list of strings representing all data labels
                labels[i] is the label of the point list_of_points[i]
        centroids_dict: a dictionary representing the centroids where the keys
                        are strings (centroid names) and the values are lists
                        of centroid locations

    Returns: a new dictionary whose keys are the centroids' key names and
             values are a list of labels of the data points that are assigned
             to that centroid.

    Example:
        Code:
            list_of_points = [[1.1, 1, 1, 0.5], [4, 3.14, 2, 1], [0, 0, 0, 0]]
            labels = ['N', 'M', 'W']
            centroids_dict = {"centroid1": [1, 1, 1, 1],
                              "centroid2": [2, 2, 2, 2]}
            print(assign_labels(list_of_points, labels, centroids_dict))
        Output:
            {'centroid1': ['M', 'N'], 'centroid2': ['W']}
    """

    label_assignments = {}

    for i in range(len(list_of_points)):
        closest = get_closest_centroid(list_of_points[i], centroids_dict)

        if closest not in label_assignments:
            label_assignments[closest] = []

        label_assignments[closest].append(labels[i])

    return label_assignments

    pass


def majority_count(labels):
    """
    Return the count of the majority label in the label list.

    Arguments:
        labels: a list of labels

    Returns: the count of the majority labels in the list

    Example:
        Given labels = ['M', 'M', 'N']
        majority_count(labels) returns 2
    """

    if len(labels) == 0:
        return 0

    label_counts = {}
    for label in labels:
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1

    max_count = 0
    for count in label_counts.values():
        if count > max_count:
            max_count = count

    return max_count
    pass


def accuracy(list_of_points, labels, centroids_dict):
    """
    Calculate the accuracy of the algorithm. You should use assign_labels and
    majority_count (that you previously implemented)

    Arguments:
        list_of_points: a list of lists representing all data points
        labels: a list of ints representing all data labels
                labels[i] is the label of the point list_of_points[i]
        centroids_dict: a dictionary representing the centroids where the keys
                        are strings (centroid names) and the values are lists
                        of centroid locations

    Returns: a float representing the accuracy of the algorithm
    """

    assigned_labels = assign_labels(list_of_points, labels, centroids_dict)

    total_majority = 0
    total_labels = len(labels)

    for centroid in assigned_labels:
        total_majority += majority_count(assigned_labels[centroid])

    return total_majority / total_labels
    pass


if __name__ == "__main__":
    centroids = load_centroids("mnist_final_centroids.csv", with_key=True)
    # Consider exploring the centroids data here

    data, label = read_data("data/mnist.csv")
    print(accuracy(data, label, centroids))

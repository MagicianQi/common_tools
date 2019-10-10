#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> DPP.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-6-18
@Intro  : Data PreProcessing Tools
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from sklearn import preprocessing
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity


def matrix_normalization(array_input, axis=0):
    """
    MinMax the input matrix in terms of dimensions.[0~1](归一化)
    :param array_input: Input numpy.array()
    :param axis: MinMax dimensions
    :return: The MinMax matrix
    """
    if type(array_input) != np.ndarray:
        raise TypeError("Data matrix format error！Not numpy.array!")
    if axis == 0:
        array_normalization = array_input / array_input.max(axis=axis)
        return array_normalization
    elif axis == 1:
        array_normalization = array_input.T / array_input.max(axis=axis)
        return array_normalization.T
    else:
        raise ValueError("Axis Value Error!")


def matrix_standardization(array_input, axis=0):
    """
    Standardized input matrix.(标准化)
    :param array_input: Input numpy.array()
    :param axis: standardized dimensions
    :return: [The Standardized matrix, mean of matrix, std of matrix]
    """
    if type(array_input) != np.ndarray:
        raise TypeError("Data matrix format error！Not numpy.array!")
    if axis == 0:
        mean = array_input.mean(axis=axis)
        std = array_input.std(axis=axis)
        # Prevent the standard deviation from being zero
        std = np.where(std == 0, 1, std)
        array_standardization = (array_input - mean) / std
        return array_standardization, mean, std
    elif axis == 1:
        mean = array_input.mean(axis=axis)
        std = array_input.std(axis=axis)
        # Prevent the standard deviation from being zero
        std = np.where(std == 0, 1, std)
        array_standardization = (array_input.T - mean) / std
        return array_standardization.T, mean, std
    else:
        raise ValueError("Axis Value Error!")


def matrix_regularization(array_input, axis=0, norm='l2'):
    """
    Regularized input matrix.(正则化)
    :param axis: Regularized dimensions
    :param array_input: Input numpy.array()
    :param norm: Regularized type
    :return: The Regularized matrix.
    """
    if type(array_input) != np.ndarray:
        raise TypeError("Data matrix format error！Not numpy.array!")
    if axis == 0:
        array_regularization = preprocessing.normalize(array_input.T, norm=norm)
        return array_regularization.T

    elif axis == 1:
        array_regularization = preprocessing.normalize(array_input, norm=norm)
        return array_regularization
    else:
        raise ValueError("Axis Value Error!")


def matrix_binarization(data_input, threshold=0.0):
    """
    Data binarization.(二值化)
    :param data_input: Input data
    :param threshold: Threshold of binarization(Less than the threshold is zero, the opposite is one)
    :return: Binary data
    """
    out_binarized = preprocessing.Binarizer(threshold=threshold).transform(data_input)
    return out_binarized


def missing_value_processing(array_input, strategy='mean', axis=0):
    """
    Missing value processing for matrix
    :param array_input: Input matrix
    :param strategy: Missing value processing strategy.['mean', 'median', 'most_frequent']
    :param axis: Missing value processing strategy dimensions.
    :return: Missing value processed matrix.
    """
    if type(array_input) != np.ndarray:
        array_input = np.array(array_input)
    Iop = preprocessing.Imputer(missing_values='NaN', strategy=strategy, axis=axis)
    array_processed = Iop.fit_transform(array_input)
    return array_processed


def label_encoder(vector):
    """
    Vector elements are converted to integers
    :param vector: Input vector
    :return: Output vector
    """
    if type(vector) != np.ndarray:
        vector = np.array(vector)
    encoder = preprocessing.LabelEncoder()
    integer_encoded = encoder.fit_transform(vector)
    return integer_encoded


def one_hot_encoder(vector, sparse=False):
    """
    One-hot coding of vectors
    :param vector: Input vector
    :param sparse: Whether the sparse matrix is returned
    :return: Output matrix
    """
    vector = label_encoder(vector)
    encoder = preprocessing.OneHotEncoder(sparse=sparse)
    integer_encoded = vector.reshape(len(vector), 1)
    onehot_encoded = encoder.fit_transform(integer_encoded)
    return onehot_encoded


def calculate_vector_cosine_similarity(embedding_a, embedding_b):
    """
    Calculate vector cosine_similarity
    :param embedding_a: Vector a
    :param embedding_b: Vector b
    :return: Similarity
    """
    cos = np.dot(embedding_a, embedding_b) / (np.linalg.norm(embedding_a) * (np.linalg.norm(embedding_b)))
    sim = 0.5 + 0.5 * cos
    return sim


def calculate_vector_euclidean_distance(embedding_a, embedding_b):
    """
    Calculate vector euclidean_distance
    :param embedding_a: Vector a
    :param embedding_b: Vector b
    :return: Distance
    """
    diff = np.subtract(embedding_a, embedding_b)
    dist = np.sum(np.square(diff), 1)
    return dist


def calculate_matrix_cosine_similarity(matrix_a, matrix_b):
    """
    Calculate matrix cosine_similarity
    :param matrix_a: Matrix a
    :param matrix_b: Matrix b
    :return: Similarity
    """
    return cosine_similarity(matrix_a, matrix_b)


def calculate_matrix_euclidean_distance(matrix_a, matrix_b):
    """
    Calculate matrix euclidean_distance
    :param matrix_a: Matrix a
    :param matrix_b: Matrix b
    :return: Distance
    """
    return euclidean_distances(matrix_a, matrix_b)


if __name__ == "__main__":
    a = np.array([[1, 5, 2, 2],
                  [1, 2, 5, 4],
                  [1, 5, 8, 5]])
    print(missing_value_processing(a))


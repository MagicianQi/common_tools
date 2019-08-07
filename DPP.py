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


if __name__ == "__main__":
    a = np.array([[1, 1, 2, 2],
                  [1, 2, 3, 4],
                  [1, 5, 8, 10]])
    print(matrix_binarization(a, 1.9))


# -*- coding: utf-8 -*-

"""=================================================
@Project -> File   ：tools -> TF_Keras_Utils.py
@IDE    : Pycharm
@Author : Qi Shuo
@Date   : 2019-10-31
@Intro  : Keras and TensorFlow utils
=================================================="""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow as tf

from keras.models import load_model
from keras import backend as K


def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.

    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.
    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
                          or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = tf.graph_util.convert_variables_to_constants(
            session, input_graph_def, output_names, freeze_var_names)
        return frozen_graph


def keras2pb(keras_model_path, output_path, pb_file_name):
    """
    Transform .h5 to .pb
    :param keras_model_path: Input keras model file path
    :param output_path: Output pb file dir
    :param pb_file_name: Output pb file name
    :return: None
    """
    model = load_model(keras_model_path)
    frozen_graph = freeze_session(K.get_session(), output_names=[out.op.name for out in model.outputs])
    tf.train.write_graph(frozen_graph, output_path, pb_file_name, as_text=False)


def print_tensor_of_pb(pb_file_path, gpu_id='0'):
    """
    Print Tensor name of Graph
    :param pb_file_path: Input pb file path
    :param gpu_id: Device load graph
    :return: None
    """
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_id
    with tf.gfile.GFile(pb_file_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    graph = tf.Graph()
    with graph.as_default():
        tf.import_graph_def(graph_def)
        print([n.name for n in tf.get_default_graph().as_graph_def().node])


def pb2savedmodel4serving(pb_file_path, input_tensor_name, output_tensor_name, saved_model_path="./saved_model_path", gpu_id='0'):
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_id

    with tf.gfile.GFile(pb_file_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    graph = tf.Graph()
    with graph.as_default():
        # ---------------Add layers in front of the Graph---------------
        # input_bytes = tf.placeholder(tf.string, shape=(), name='input_images')
        # decoded_image = tf.image.decode_jpeg(tf.reshape(input_bytes, []), channels=3)
        # decoded_image = tf.cast(decoded_image, tf.float32)
        # decoded_image = decoded_image / 255.
        # decoded_image = tf.expand_dims(decoded_image, 0)
        # tf.import_graph_def(graph_def, input_map={"input_1:0", decoded_image})
        # ---------------------------------------------------------------

        tf.import_graph_def(graph_def)
        input_tensor = graph.get_tensor_by_name(input_tensor_name)  # "input_1:0"
        output_tensor = graph.get_tensor_by_name(output_tensor_name)  # "import/predictions/Softmax:0"

        with tf.Session() as sess:
            builder = tf.saved_model.builder.SavedModelBuilder(saved_model_path)

            model_input = tf.saved_model.utils.build_tensor_info(input_tensor)
            model_output = tf.saved_model.utils.build_tensor_info(output_tensor)

            model_signature = tf.saved_model.signature_def_utils.build_signature_def(
                inputs={
                    'input': model_input
                },
                outputs={
                    'prediction': model_output
                },
                method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME
            )

            builder.add_meta_graph_and_variables(
                sess,
                [tf.saved_model.tag_constants.SERVING],
                signature_def_map={
                    tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: model_signature
                },
                main_op=tf.tables_initializer(),
                strip_default_attrs=True
            )
            builder.save()

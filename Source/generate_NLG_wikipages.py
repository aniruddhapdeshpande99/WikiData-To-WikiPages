# Importing Libraries and needed utilities
from Summary_Generator.Tensorflow_Graph import order_planner_with_copynet
from Summary_Generator.Text_Preprocessing_Helpers.pickling_tools import *
from Summary_Generator.Text_Preprocessing_Helpers.utils import *
from Summary_Generator.Tensorflow_Graph.utils import *
from Summary_Generator.Model import *
import numpy as np
import tensorflow as tf
import json

def retrieve_nlg_output(model_directory, model_meta, X, Y, mem_fraction, content_label_vocabulary, start):

    train_X_field = X[0]
    train_X_content = X[1]
    train_Y = Y

    # Tensor Configuration
    tensor_config = tf.ConfigProto()
    tensor_config.gpu_options.allow_growth = False
    tensor_config.gpu_options.per_process_gpu_memory_fraction = mem_fraction

    # Loading the weights and graph and retrieving predicted wikipages
    with tf.Session(config=tensor_config) as sess:
        saver = tf.train.import_meta_graph(model_meta)
        saver.restore(sess, tf.train.latest_checkpoint(model_directory))

        graph = tf.get_default_graph()

        inp_field_encodings = graph.get_tensor_by_name('Input_Data/input_field_encodings:0')
        inp_content_encodings = graph.get_tensor_by_name('Input_Data/input_content_encodings:0')
        inp_label_encodings = graph.get_tensor_by_name('Input_Data/input_label_encodings:0')
        inp_sequence_lengths = graph.get_tensor_by_name('Input_Data/input_sequence_lengths:0')
        lab_sequence_lengths = graph.get_tensor_by_name('Input_Data/decoder_sequence_lengths:0')

        outputs = graph.get_tensor_by_name('Training_computations/transpose:0')

        no_of_total_examples = len(train_X_field)
        end = start+1

        inp_field = pad_sequences(train_X_field[start: end])
        inp_conte = pad_sequences(train_X_content[start: end])
        inp_label = pad_sequences(train_Y[start: end])
        inp_lengths = get_lengths(train_X_field[start: end])
        lab_lengths = get_lengths(train_X_content[start: end])


        predicts = sess.run(outputs, feed_dict = {
        inp_field_encodings: inp_field,
        inp_content_encodings: inp_conte,
        inp_label_encodings: inp_label,
        inp_sequence_lengths: inp_lengths,
        lab_sequence_lengths: lab_lengths
        })

        random_index = np.random.randint(len(inp_field))

        random_label_sample = inp_label[random_index]
        random_predicts_sample = np.argmax(predicts, axis = -1)[random_index]


        hypotheses = reduce(lambda x,y: x + " " + y, [content_label_vocabulary[label] for label in random_predicts_sample])
        references = reduce(lambda x,y: x + " " + y, [content_label_vocabulary[label] for label in random_label_sample])

        # print the extracted sample in meaningful format
        print("\nOriginal Summary: ")
        print(references)

        print("\nPredicted Summary: ")
        print(hypotheses)

        return hypotheses

# Dataset Path
data_path = "../Data/Films/WikiBio_Styled_Formatted_Data/train/"
plug_and_play_data_file = os.path.join(data_path, "plug_and_play.pickle")

# Reading and unpickckling Data
print("Unpickling the data from the disc ...")
data = unPickleIt(plug_and_play_data_file)

# Inputs needed to be sent to retrieve the interface_dict in order to
# put inputs to the graph.
field_encodings = data['field_encodings']
field_dict = data['field_dict']
content_encodings = data['content_encodings']
label_encodings = data['label_encodings']
content_label_dict = data['content_union_label_dict']
rev_content_label_dict = data['rev_content_union_label_dict']

# Vocabulary sizes
field_vocab_size = data['field_vocab_size']
content_label_vocab_size = data['content_label_vocab_size']

train_percentage = 100

X, Y = zip(field_encodings, content_encodings), label_encodings
train_X, train_Y = X, Y
train_X_field, train_X_content = zip(*train_X)
train_X_field = list(train_X_field); train_X_content = list(train_X_content)

# Free up the resources by deleting non required stuff
del X, Y, field_encodings, content_encodings, train_X
print("\nTotal_training_examples:", len(train_X_field))

mem_fraction = 0.2

# Testing and retrieving outputs
model_meta = '../Models/Films_Weights/Model_1(without_copy_net)-6899.meta'
model_directory = '../Models/Films_Weights/'

wiki_article = {}
with open('../Data/Films/temp.json') as f:
    wiki_article = json.load(f)

nlg_output = retrieve_nlg_output(model_directory, model_meta, (train_X_field, train_X_content), train_Y, mem_fraction, content_label_dict, wiki_article['film_details']['index'])
with open('../Data/Films/temp2.json', 'w') as f:
    json.dump(nlg_output,f)

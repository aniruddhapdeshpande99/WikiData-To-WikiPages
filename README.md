# KG to Text: Wikidata to Wikipedia Pages

This project of Automatic text generation from Knowledge graphs aims to study, capture and convert the information stored in the form of Wikidata Knowledge graphs to that of Hindi Wikipedia pages. Final Wikipage generation task involved both usage of template based sentence generation and generation using a Natural Language Generator based on the paper - "Order-Planning Neural Text Generation From Structured Data." 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. For further details about the project, please read the Documentation explaining our approach and explanations about the functions written for this project. 

The Model size exceeds Github's maximum file size and hence needs to be downloaded separately using the link below:

* [Saved Weights](https://drive.google.com/open?id=10vcg-X2h4WuFE3CTfgXLB-XsfXNzvylA)
* Place the 'Film_Weights' directory in 'Models' directory.

### Prerequisites

* The Code requires you to have both Python2.7 and Python3.5 in your system. The NLG network was coded and trained on Python2.7, and the Python Notebooks on Python3.5.
* To run the the .ipynb Python notebooks, please install Jupyter Notebook based on the instructions [here](https://jupyter.readthedocs.io/en/latest/install.html)
* Required Python2.7 Libraries

```
Package              Version
-------------------- ---------
absl-py              0.9.0
astor                0.8.1
backports.weakref    1.0.post1
click                7.1.1
enum34               1.1.10
funcsigs             1.0.2
futures              3.3.0
gast                 0.3.3
grpcio               1.28.1
h5py                 2.10.0
joblib               0.14.1
Keras                2.3.1
Keras-Applications   1.0.8
Keras-Preprocessing  1.1.0
Markdown             3.1.1
mock                 3.0.5
nltk                 3.5
numpy                1.16.6
pip                  20.0.2
protobuf             3.11.3
PyYAML               5.3.1
regex                2020.4.4 
scipy                1.2.3
setuptools           44.1.0
six                  1.14.0
tensorboard          1.13.1
tensorflow           1.13.2
tensorflow-estimator 1.13.0
termcolor            1.1.0
tqdm                 4.45.0
Werkzeug             1.0.1
wheel                0.34.2
```
* Required Python3.5 Libraries

```
Package              Version
-------------------- ---------
requests             2.23.0
beautifulsoup4       4.7.1
googletrans          2.4.0
nltk                 3.5
qwikidata            0.4.0
```

### Training
* To preprocess before training ,run the following. 

```
python fast_data_preprocessor_part1.py
python fast_data_preprocessor_part2.py

```

* To train the network without Copy Mechanism, run the following.
```
python trainer_without_copy_net.py

```

* To train the network with Copy Mechanism, run the following.
```
python trainer_with_copy_net.py

```

* To display any random wikipage run the following shell script in Main Project Directory.
```
./display_random_wiki.sh
Run 'index.html' in your browser.

```
* To run the Python Notebooks use the following.
```
jupyter notebook

```
* In your browser run and use the notebooks.


## Authors

* **Aniruddha Deshpande** [Github Profile](https://github.com/aniruddhapdeshpande99)
* **Aditya Agarwal** [Github Profile](https://github.com/aditya3498)

See also the list of [contributors](https://github.com/aniruddhapdeshpande99/WikiData-To-WikiPages/graphs/contributors) who participated in this project.

## Acknowledgments

* We would like to thank Prof. Vasudeva Verma for his continued support.
* We also would like to thank our TA Mentors - Tushar Abhishek, Nikhil Pattisapu for all their help.


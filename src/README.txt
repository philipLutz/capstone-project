The goal of this project is to make predictions about runtime program behavior based on features from static analysis. 

Each program in "test-programs" is a sample.

The metrics from Frama-C will be used as input features.

The runtime performance data will be transformed to a single real number score to describe how significantly a program's
runtime is influenced by CPU frequency. Each score will be assigned a class based on its order of magnitude.
A program that is more CPU-bound will have a smaller score than a program that is memory-bound or IO-bound.
Each sample program is run multiple times, and the average of the runs is used to compute the score.

I am planning to use supersived machine learning techniques to predict runtime performance scores.

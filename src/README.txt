The goal of this project is to make predictions about runtime program behavior based on features from static analysis. 

Each program in "test-programs" is a sample.

The metrics from Frama-C will be used as input features.

The runtime performance data will be transformed to a single real number score to describe how significantly a program's
runtime is influenced by CPU frequency. A program that is more CPU-bound will have a higher score than a program that
is memory-bound or IO-bound. 

I am planning to use classical supersived machine learning techniques to predict runtime performance scores.

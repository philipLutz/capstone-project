"""
Create Dataset for Machine Learning Model Training and Testing
Correctly order and pair static analysis results (inputs) with performance scores (outputs)
Two resulting CSV files are created
"""

import csv


SCORES_FILE = "program_scores.csv"
ANALYSIS_RESULTS = "static_analysis_results.csv"
OUTPUT_X_FILE = "x_all.csv"
OUTPUT_Y_FILE = "y_all.csv"

# Sort the rows from performance scores and static analysis results so the ordering matches each program sample
inputs = []
inputs_header = ""
outputs = []
outputs_header = ""

with open(ANALYSIS_RESULTS, 'r', newline='') as inputs_file:
    reader = csv.reader(inputs_file, delimiter=',')
    i = 0
    for row in reader:
        if i == 0:
            inputs_header = ", ".join(row)
        else:
            inputs.append(", ".join(row))
        i += 1

inputs.sort()
inputs.insert(0, inputs_header)

with open(SCORES_FILE, 'r', newline='') as outputs_file:
    reader = csv.reader(outputs_file, delimiter=',')
    i = 0
    for row in reader:
        if i == 0:
            outputs_header = ", ".join(row)
        else:
            outputs.append(", ".join(row))
        i += 1

outputs.sort()
outputs.insert(0, outputs_header)

# Check that the sorting correctly matches the rows from both files
for i in range(len(inputs)):
    is_match = True
    j = 0
    while inputs[i][j] != ',':
        if inputs[i][j] != outputs[i][j]:
            is_match = False
            break
        
        j += 1
    if not is_match:
        print("NOT MATCHED")
        print(inputs[i])
        print(outputs[i])


# Write the data to two files for model training and testing
with open(OUTPUT_X_FILE, 'w', newline='') as x_file:
    writer = csv.writer(x_file, delimiter=',')
    for i in range(len(inputs)):
        line_to_write = inputs[i].split(', ')
        # remove program name
        del line_to_write[0]
        # remove file-error column
        del line_to_write[-2]
        writer.writerow(line_to_write)

with open(OUTPUT_Y_FILE, 'w', newline='') as y_file:
    writer = csv.writer(y_file, delimiter=',')
    for i in range(len(outputs)):
        line_to_write = outputs[i].split(', ')
        # remove program name
        del line_to_write[0]
        writer.writerow(line_to_write)


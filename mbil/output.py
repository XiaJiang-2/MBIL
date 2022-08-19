from datetime import date
today = date.today()
def output(dataset_name, allinput, datasetpath, dataset_information, null_score, single_score, interaction_score,interaction_information_gain, true_parent):
    lines = ['Readme', 'How to write text files in Python']
    file_name = dataset_name + str(today.strftime("%b-%d-%Y"))
    with open('output/'+ file_name + '.txt', 'w') as f:
        f.write("The user entered values for the parameters:")
        for key, val in allinput.items():
            f.write(str(key) + ": " + str(val))
            f.write('\n')
        f.write('\n')
        f.write("Current dataset path:" + datasetpath)
        f.write('\n')
        for key, val in dataset_information.items():
            f.write(str(key) + ": " + str(val))
            f.write('\n')
        f.write('\n')
        f.write("Null Score:" + str(null_score))
        f.write('\n')
        f.write("Now printing the score of each of the single predictor models:")
        f.write('\n')
        for item in single_score:
            f.write(str(item))
            f.write('\n')
        f.write('\n')
        f.write("Now printing interactions and their scores learned by IGain:")
        f.write('\n')
        for item in interaction_score:
            f.write(str(item))
            f.write('\n')
        f.write('\n')
        f.write("Now printing IGain Score of a model learned by IGain:")
        f.write('\n')
        for key, val in interaction_information_gain.items():
            f.write(str(key) + ": " + str(val))
            f.write('\n')
        f.write('\n')

        f.write("True Parents Identified: " + str(true_parent))






        # for line in lines:
        #     f.write(line)
        #     f.write('\n')
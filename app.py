import collections
import math
from collections import defaultdict, Counter
import pandas as pd
import itertools

# Output: should be natural log of score


from mbil import scores
from mbil import dataset
from mbil import search
from mbil import scores_abs
from mbil import output

#
#dataset_input_directory = "datasets/TEST.txt"
#output_directory = "C:/Users/CHX37/Practice"

dataset_input_directory="C:/Users/CHX37/PycharmProjects/MBIL/datasets/TEST.txt"
#dataset_input_directory="/Users/xij6/Documents/Research/git/XiaJiang-2Github/MBIL/datasets/TEST.txt"
alpha = 4
target = "E"
top = 20
max_single_predictors = 20
max_interaction_predictors = 20
max_size_interaction = 3
threshold = 0.05
maximum_number_of_parents=7



# dataset_input_directory = "datasets/LSM-15Year.txt"
# alpha = 240
# target = "distant_recurrence"
# top = 20
# max_single_predictors = 20
# max_interaction_predictors = 20
# max_size_interaction = 3
# threshold = 0.05
# maximum_number_of_parents=7


#subset_size_list = [0, 1, 2]


#self, threshold, max_single_predictors, max_interaction_predictors, max_size_interaction,dataset_input_directory, alpha, target):
dataset_df = dataset.ReadDataset(file=dataset_input_directory, sep='\t').dataset_df
#score = scores.BDeuScore(dataset_df=dataset_df, alpha=alpha, target=target)
score = scores_abs.utils(dataset_df=dataset_df, target=target,alpha = alpha)
# score_abs is the kind of like tha abstract class to finish basic calculation work which can be reused by other function in the future
# search_test_object is the class to do the final search according to calculation result from score_abs class
search_test_object = search.mbilsearch(threshold=threshold,
                       max_single_predictors= max_single_predictors,
                       max_interaction_predictors=max_interaction_predictors,
                       max_size_interaction= max_size_interaction,
                       dataset_df = dataset_df,
                       alpha = alpha,
                       target = target)



null_score = score.calculate_score(top = top, subset_size = 0)


ir_score_size1 = score.calculate_score(top = top, subset_size = 1)
ig_score_size1 = score.calculate_information_gain(top = top,subset_size = 1)

print("ir_score for subset size 1")
print(ir_score_size1)
print("ig_score for subset size 1")
print(ig_score_size1)
ir_score_size2 = score.calculate_score(top = top, subset_size = 2)
ig_score_size2 = score.calculate_information_gain(top = top,subset_size = 2)
print("ir_score for subset size 2")
print(ir_score_size2)
print("ig_score for subset size 2")
print(ig_score_size2)
print("Now printing the Bayesian Score of sigle predictor during the exaustive search: ")
single_list_score = search_test_object.single_list_score
print(single_list_score)
print("Now printing the Bayesian Score of interaction predictor during the exaustive search: ")
interaction_list_score = search_test_object.interaction_list_score
print(interaction_list_score)
## plot function
# score.plot_score(2)
# score.plot_information_gain(2)
search_test_object.plot_score_aftersearch()
search_test_object.plot_information_gain_aftersearch()
print("new dataset after search")
print(search_test_object.new_dataset)
print("dataset status")
print(search_test_object.new_status_dataset)

#print(search_test_object.transformed_dataset)


direct_cause_obj = search.directCause(
    new_dataset = search_test_object.transformed_dataset,
    alpha= alpha,
    target = target,
    maximum_number_of_parents = maximum_number_of_parents)
print("Now printing the true parents")
print(direct_cause_obj.direc_cause)

##########################################
interaction_information_gain = {}
for i in range(1, max_size_interaction + 1):
    name = "size" + str(i)
    interaction_information_gain[name] = score.calculate_information_gain(top = top,subset_size = i)
dataset_name = "TEST"
all_input_hash_map = {"alpha": alpha,"target":target, "top":top, "max_single_predictors":max_single_predictors, "max_interaction_predictors":max_interaction_predictors, "max_size_interaction":max_size_interaction, "threshold":threshold, "maximum_number_of_parents":maximum_number_of_parents}
number_of_predictors = dataset_df.shape[1] - 1
number_of_records = dataset_df.shape[0]
predictors_records_number = {"number_of_predictors":number_of_predictors, "number_of_records":number_of_records}
output.output(  dataset_name=dataset_name,
                allinput =all_input_hash_map,
                datasetpath = dataset_input_directory,
                dataset_information = predictors_records_number,
                null_score = null_score,
                single_score = ir_score_size1,
                interaction_score = interaction_list_score,
                interaction_information_gain = interaction_information_gain,
                true_parent = direct_cause_obj.direc_cause
       )

# ir_score = score.calculate_score(top = top, subset_size = 2)
# ig_score = score.calculate_information_gain(top = top,subset_size = 2)
# print("ir_score for subset size 2")
# print(ir_score)
# print("ig_score for subset size 2")
# print(ig_score)
# print("interaction_strength")
# print(score.interaction_strength)
# print("top_single_list")
#print(search.top_single_list)
# print("top_interaction_list")
# print(search.top_interaction_list)
# print("true_parents")
# print(true_parents.true_parents)

# res = search.get_top_singel_predictors_score()
#res = search.get_top_interaction_predictors_score()
# print(search.top_single_list)
# print(search.top_interaction_list)
# search.get_new_dataset_after_transform()
# print(search.new_dataset)
# print(search.new_status_dataset)
# ir_score = score.calculate_score(top = top, subset_size = 2)
# ig_score = score.calculate_information_gain(top = top,subset_size = 2)
#strength_score = score.calculate_interaction_strength(threshold = threshold,subset_size = 5)

# print(ir_score)
# print(ig_score)
#print(strength_score)
# print(ir_score_2)
# print(ir_score_1)
# print(ir_score_3)
# subset_size_list = [1]
# subset_size = 2
# res1 = {}
# res2 = {}
# for subset_size in subset_size_list:
#     score = BDeuScore(dataset_input_directory, alpha, target, subset_size)
#     ir_score = score.calculate_score()
#     res1.update(ir_score)
#     # res1.append(ir_score)
#     ig_score = score.calculate_information_gain()
#     res2.update(ig_score)
#     # res2.append(ig_score)
# res1_sorted = sorted(res1.items(), key=lambda item: item[1])
# res2_sorted = sorted(res2.items(), key=lambda item: item[1])
# print(res1_sorted[:top])
# print(res2_sorted[:top])

















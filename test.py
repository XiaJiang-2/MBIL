from mbil import scores
from mbil import dataset
from mbil import mbilsearch
from mbil import mbilscore


# dataset_input_directory = "datasets/TEST.txt"
# output_directory = "C:/Users/CHX37/Practice"
# alpha = 4
# target = "E"

# subset_size = [1,2,3]

# top = 20
# threshold = 0.05

dataset_input_directory = "datasets/LSM-15Year.txt"
alpha = 240
target = "distant_recurrence"
threshold=0.05
subset_size = 3
top = 20


#subset_size_list = [0, 1, 2]

#score = BDeuScore.BDeuScore(dataset_input_directory = dataset_input_directory, alpha = alpha, target = target)
#self, threshold, max_single_predictors, max_interaction_predictors, max_size_interaction,dataset_input_directory, alpha, target):
dataset_df = BDeuScore.ReadDataset(file=dataset_input_directory, sep='\t').dataset_df
score = BDeuScore.BDeuScore(dataset_df=dataset_df, alpha=alpha, target=target)
search = BDeuScore.Search(threshold=threshold,max_single_predictors= 20,max_interaction_predictors=20, max_size_interaction= 3,dataset_df = dataset_df, alpha = alpha, target = target)
true_parents = BDeuScore.TrueParents(search.transformed_dataset, alpha= alpha, target = target, maximum_number_of_edges=7)
# ir_score = score.calculate_score(top = top, subset_size = 2)
# ig_score = score.calculate_information_gain(top = top,subset_size = 2)
# print("ir_score for subset size 2")
# print(ir_score)
# print("ig_score for subset size 2")
# print(ig_score)
print("interaction_strength")
print(score.interaction_strength)
print("top_single_list")
print(search.top_single_list)
print("top_interaction_list")
print(search.top_interaction_list)
print("true_parents")
print(true_parents.true_parents)
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

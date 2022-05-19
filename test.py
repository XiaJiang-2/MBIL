from scores import BDeuScore

# dataset_input_directory = "../datasets/TEST.txt"
dataset_input_directory = "datasets/LSM-15Year.txt"
output_directory = "C:/Users/CHX37/Practice"
# alpha = 4
alpha = 240
# target = "E"
target = "distant_recurrence"
subset_size = 1
#subset_size_list = [0, 1, 2]
top = 20

score = BDeuScore.BDeuScore(dataset_input_directory, alpha, target, subset_size)
ir_score = score.calculate_score(top = top)
ig_score = score.calculate_information_gain(top = top)
print(ir_score)
print(ig_score)
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

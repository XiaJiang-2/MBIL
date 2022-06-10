import collections
import math
from collections import defaultdict, Counter
import pandas as pd
from mbil import scores
from mbil import scores_abs

import itertools

# Output: should be natural log of score


class TrueParents:
    def __init__(self, new_dataset,alpha,target,maximum_number_of_parents):
        self.new_dataset = new_dataset
        self.parent_list = list(self.new_dataset.columns)
        self.target = target
        self.alpha = alpha
        self.parent_list.remove(self.target)
        self.score = scores.BDeuScore(dataset_df=self.new_dataset, alpha=self.alpha, target=self.target)
        self.utils = scores_abs.utils(dataset_df=self.new_dataset,target=self.target, alpha = self.alpha)
        self.maximum_number_of_parents = maximum_number_of_parents
        self.true_parents = self.detecting_true_parents()


    def detecting_true_parents(self):
        # parent_list will be B  ['B', 'C']  ['B', 'F']  ['C', 'D']  ['D', 'F']  ['C', 'F']  E
        # 1. ["BC" ,"BF", "DF", "CD","CF",0,]
        # 2. parent_list = [1,0], i = 1, [],[]
        # print(new_dataset)
        # parent_list = list(new_dataset.columns)
        # print(parent_list)
        def iterator(parent_list):
            for item in parent_list:
                yield item
        def getsubsets(input ,length):
            #print(input)
            def dfs(input, length, start_index, acc, sol):
                if (len(acc) == length):
                    sol.append(acc[:])
                    return
                if input and start_index == len(input):
                    return
                element = input[start_index]
                acc.append(element)
                dfs(input, length, start_index + 1, acc, sol)
                acc.remove(element)
                dfs(input, length, start_index + 1, acc,sol)
            res = []
            dfs(input, length, 0, [], res)
            return res

        def increaseScore(input):
            index = -1
            cur_list_score = self.score.calculate_BDeu(input)
            #print("Score computed for set "+ str(B) +" is: "+ str(cur_list_score))
            list_B = input[:]
            for item in list_B:
                copy_list = list_B[:]
                copy_list.remove(item)
                # if len(copy_list) == 0:
                #     #print("stop")
                new_score = self.score.calculate_BDeu(copy_list)
                #print("New score is " + str(copy_list) + str(new_score))
                if new_score > cur_list_score:
                    cur_list_score = new_score
                    index = list_B.index(item)
            if index != -1:
                input.remove(list_B[index])
        # parent_list =
        i = 0
        while (len(self.parent_list) > i) and (i <= self.maximum_number_of_parents):
            #self.parent_list = iterator(self.parent_list)
            for predictor in self.parent_list[:]:
                cur_parent = self.parent_list[:]
                cur_parent.remove(predictor)
                #print("cur_parent " + str(cur_parent) +" i " + str(i))
                blockersofsizeI = getsubsets(cur_parent,i)
                #print("blockersofsizeI " + str(blockersofsizeI))
                #print()
                for subset in blockersofsizeI:
                    B = []
                    if predictor in self.parent_list:
                        B = subset[:]
                        #print(predictor)
                        B.append(predictor)
                        increaseScore(B)
                        if predictor not in B:
                            self.parent_list.remove(predictor)
            i+=1
        return self.parent_list

    # self.detecting_true_parents(self.new_dataset)

class Search:
    # get top single predictors and top interaction predictors and transform dataset df and new_status_dataset
    def __init__(self, threshold, max_single_predictors, max_interaction_predictors, max_size_interaction,dataset_df, alpha, target):
        self.alpha = alpha
        self.target = target
        self.threshold = threshold
        self.dataset = dataset_df
        self.max_single_predictors = max_single_predictors
        self.max_interaction_predictors = max_interaction_predictors
        self.max_size_interaction = max_size_interaction
        self.score = scores.BDeuScore(dataset_df=dataset_df, alpha=alpha, target=target)
        self.utils = scores_abs.utils(dataset_df=self.dataset, target=self.target,alpha = self.alpha)
        #self.top_interaction_list = collections.OrderedDict()
        self.top_interaction_list = self.get_top_interaction_predictors_score()
        self.top_single_list = self.get_top_singel_predictors_score()
        # initialize the new dataset, kind of global variable
        self.new_dataset = {}
        # use get_new_dataset_after_transform to fill transform dataset
        self.transformed_dataset = self.get_new_dataset_after_transform()
        self.new_status_dataset = {}


    def get_top_singel_predictors_score(self):
        predictors_list = self.score.dataset_head
        predictors_list.remove(self.target)
        null_score = self.utils.calculate_score(subset_size=0, top="all").values()
        null_score = list(null_score)[0]
        score_dict = self.utils.calculate_score(subset_size=1, top="all")
        single_res = []

        for key,val in score_dict.items():
            if int(val) > null_score:
                single_res.append((key.strip("[]''"),val))
        return single_res

    def get_top_interaction_predictors_score(self):
        interaction_res = {}
        #score = BDeuScore(dataset_input_directory=self.dataset_input_directory, alpha=self.alpha, target=self.target)
        #number_of_predictors = score.n
        for i in range(2,self.max_size_interaction + 1):
            cur_infoGain_stren = self.score.calculate_interaction_strength(subset_size=i,dataset = self.dataset,threshold = self.threshold)
            cur_score_dict = self.utils.calculate_score(subset_size=i)
            for key,val in cur_score_dict.items():
                if key in cur_infoGain_stren:
                    interaction_res[key] = cur_score_dict[key]
        #return Counter(self.top_interaction_list).most_common(1)
        return Counter(interaction_res).most_common(self.max_interaction_predictors)

    def get_new_dataset_after_transform(self):
        def generate_inter_list(interaction):
            interaction = list(interaction[0][1:-1].split(", "))
            new_col = []
            for i in range(self.score.m):
                new_val = ""
                for item in interaction:
                    item = item.strip("'")
                    new_val += str(self.score.dataset_df[item][i])

                new_col.append(new_val)
            return new_col

        def generate_new_status_dataset(newdataset):
            newdataset_matrix = list(newdataset.values())
            m = len(newdataset_matrix)
            n = len(newdataset_matrix[0])
            new_status_dataset = [[0 for _ in range(n) ] for _ in range(m)]
            for i in range(m):
                status_size = len(set(newdataset_matrix[i]))
                status_set = list(set(newdataset_matrix[i]))
                status_set_add_size = [status_size]
                #print(status_set_add_size)
                status_set_add_size.extend(status_set)
                for j in range(len(status_set_add_size)):
                    new_status_dataset[i][j] = status_set_add_size[j]
            return new_status_dataset


        # score = BDeuScore(dataset_input_directory=self.dataset_input_directory, alpha=self.alpha, target=self.target)

        #new_dataset = collections.defaultdict(list)
        #self.new_dataset = {}
        for item in self.top_single_list:
            new_col = []
            hash_table = {}
            i = 0
            feature_original_list = list(self.score.dataset_df[item[0]])
            for val in feature_original_list:
                if val not in hash_table:
                    hash_table[val] = i
                    i += 1
                new_col.append(hash_table[val])
            self.new_dataset[item[0]] = new_col
        # print(new_dataset)
        for item in self.top_interaction_list:
            new_feature_list = generate_inter_list(item)
            new_col = []
            hash_table = {}
            i = 0
            for val in new_feature_list:
                if val not in hash_table:
                    hash_table[val] = i
                    i += 1
                new_col.append(hash_table[val])
            self.new_dataset[item[0]] = new_col
        self.new_dataset[self.score.target] = list(self.score.dataset_df[self.score.target])
        self.new_status_dataset = generate_new_status_dataset(self.new_dataset)
        #print(self.new_dataset)
        self.new_dataset = pd.DataFrame(self.new_dataset)
        # format the key from "['B','C']" to "BC"
        # for key,val in self.new_dataset.items():
        #     key = key[1:-1].split(',')
        #     print(key)
        return self.new_dataset






















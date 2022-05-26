import collections
import math
from collections import defaultdict, Counter
import pandas as pd
import itertools

# Output: should be natural log of score

# example dataset E is the target
# B	 C	D	F	E
# 2	 1	0	1	0
# 3	 1	1	2	1
# 3	 0	1	1	0
# 3	 0	1	1	1
# 2	 1	2	2	0

class BDeuScore:
    def __init__(self,dataset_input_directory="../datasets/TEST.txt", alpha=4.0, target="E"):
        '''
        init function of BDeuScore class

        :param dataset_input_directory: the directory of the dataset you want to use
        :param alpha: A parameter of Bayesian score
        :param target: the name of the target you want to use, the target must be included in dataset
        :param subset_size: the size of the subset

        '''
        self.alpha = alpha
        self.dataset_input_directory = dataset_input_directory
        self.target = target
        self.dataset_df = self.readDataset(file=dataset_input_directory, sep='\t')
        self.dataset_head = list(self.dataset_df.columns)
        self.m = self.dataset_df.shape[0]
        self.n = self.dataset_df.shape[1]
        self.interaction_strength = {}


    def readDataset(self, file, sep='\t'):
        '''
        A function to read the dataset according to the input directory of this dataset

        :param file: input directory of this dataset
        :param sep: the delimiter of the dataset like '\t' or ',', default='\t'

        :return dataset: the dataset with data frame format in python
        '''
        dataset_df = pd.read_csv(filepath_or_buffer=file, sep=sep, lineterminator='\n')
        columns_name = list(dataset_df.columns)
        columns_name[-1] = columns_name[-1].strip()
        dataset_df.columns = columns_name
        # dataset_df = pd.read_csv(file, sep)
        # dataset_df = dataset_df.iloc[:, :-1]
        #dataset_df = dataset_df.iloc[:,:-1]
        #print(f'dataset directory: {file}')
        #print(f'dataset shape: {dataset_df.shape}')
        #print(f'dataset dimension: {dataset_df.ndim}')

        return dataset_df


    def generate_subset(self, feature_list, subset_size):
        '''
        A function to generate all posiible subset according to the subset_size

        :param feature_list: the list that includes all features in the dataset, it will be ["B", "C", "D"] based on example dataset
        :param subset_size:  the size of the subset you want to generate

        :return list: a list that include all possible subset, if the subset_size == 2, it will be [["B", "C"], ["B", "D"], ["C", "D"]]
        '''
        if subset_size == 0:
            return [[]]
        def dfs(index, cur):
            if len(cur) == subset_size:
                result.append(cur[:])
                return
            for i in range(index, len(feature_list)):
                dfs(i + 1, cur + [feature_list[i]])

        index = 0
        cur = []
        result = []
        dfs(index, cur)
        return result

    def calculate_informationgain_each_subset(self, subset, dataset_model):
        if len(subset) == 0:
            score = 1
        else:
            score = 0
            subset_status_map = dataset_model.get_subset_status()
            parent_set = dataset_model.get_parent(subset_status_map)
            target_status_list = dataset_model.get_target_status()
            unique_value_count_onefeature_map = dataset_model.get_feature_count(dataset_model.target)
            jointCounts = [0] * len(target_status_list)
            classifierProbabilities = [0] * len(target_status_list)
            for parent in parent_set:
                sumCounts = 0
                i = 0
                for target_status in target_status_list:
                    #print(classifierProbabilities[i])
                    if classifierProbabilities[i] == 0:
                        classifierProbabilities[i] = unique_value_count_onefeature_map[target_status] / self.m
                    count = dataset_model.get_all_count(subset, parent, target_status)
                    jointCounts[i] = count
                    sumCounts += jointCounts[i]
                    i += 1
                if sumCounts == 0:
                    continue
                parentCountProb = sumCounts / self.m
                for k in range(len(target_status_list)):
                    jointCount = jointCounts[k]
                    if jointCount == 0:
                        continue
                    jointCountProb = jointCount/self.m
                    # print("jointCountProb")
                    # print(jointCountProb)
                    # print(classifierProbabilities)
                    # print(classifierProbabilities[k])
                    # print(math.log2(parentCountProb))
                    logscore = jointCountProb * (math.log2(jointCountProb) - (math.log2(classifierProbabilities[k]) + math.log2(parentCountProb)))
                    score += logscore
        return score

    def calculate_information_gain(self,subset_size,top = "all"):
        '''
        A function to calculate information gain

        :param self: instance of BDeuScore class

        :return score: the score
        '''

        m = self.dataset_df.shape[0]
        feature_list_excepet_target = list(self.dataset_df.columns)
        res = {}

        #print(feature_list_excepet_target)
        feature_list_excepet_target.remove(self.target)
        subset = self.generate_subset(feature_list_excepet_target, subset_size)

        for each_com in subset:
            score = 0
            if len(each_com) == 0:
                score = 1
            else:
                dataset_model = Dataset(self.dataset_df, self.target, each_com)
                score = self.calculate_informationgain_each_subset(each_com, dataset_model)
            res[str(each_com)] = score

        if top == 'all':
            return res
        else:
            return sorted(res.items(), key=lambda item: item[1], reverse=True)[:top]



    def calculate_score_each_subset(self, each_com, dataset_model):
        subset_status_map = dataset_model.get_subset_status()
        parent_set = dataset_model.get_parent(subset_status_map)
        target_status_list = dataset_model.get_target_status()
        unique_value_count_onefeature_map = dataset_model.get_feature_count(dataset_model.target)
        score = 0
        # calculate null_score
        if each_com:
            q = 1
            for key, val in subset_status_map.items():
                q *= len(val)
            alphaijk = self.alpha / q
            # self.alpha/ q * r(the status of the )
            alphaijkri = self.alpha / (q * len(target_status_list))
            gammaAlphaijk = math.lgamma(alphaijk)
            gammaAlphaijkri = math.lgamma(alphaijkri)
            # {D:[0,1]}
            # hash_table = collections.defaultdict(int)
            # parent_set = [[0,1],[]]
            for parent in parent_set:
                sumOfSijk = 0
                temptemp = 0
                tempscore = 0
                for target_status in target_status_list:
                    # key = feature_name + str(val) + "classifier" + str(status)
                    count = dataset_model.get_all_count(each_com, parent, target_status)
                    # print(count)
                    if not count:
                        continue
                    sumOfSijk += count
                    sumOfAalphaijkri = alphaijkri + count
                    gammaSumri = math.lgamma(sumOfAalphaijkri)
                    finalProduct = gammaSumri - gammaAlphaijkri

                    temptemp += finalProduct
                # print(temptemp)
                sumOfAlphaAndSumSijk = alphaijk + sumOfSijk
                gammaSum = math.lgamma(sumOfAlphaAndSumSijk)
                tempscore = gammaAlphaijk - gammaSum
                tempscore += temptemp
                score += tempscore
            # print(str(each_com) + " score is " + str(score))
        else:
            q = 1
            sijk_sum = 0
            alphaijk = self.alpha / q
            alphaijkri = self.alpha / (q * len(target_status_list))
            gammaAlphaijk = math.lgamma(alphaijk)
            gammaAlphaijkri = math.lgamma(alphaijkri)
            temp_score = 0
            temptemp = 0
            for classifier_value in target_status_list:
                classifier_count = unique_value_count_onefeature_map[classifier_value]
                if classifier_count == 0:
                    continue
                sijk_sum += classifier_count
                alphaijkri_sum = alphaijkri + classifier_count
                sumri_lgamma = math.lgamma(alphaijkri_sum)
                final_product = sumri_lgamma - gammaAlphaijkri
                temptemp += final_product
            alphaijkAndSumSijk_sum = alphaijk + sijk_sum
            alphaijkAndSumSijk_sum_lgamma = math.lgamma(alphaijkAndSumSijk_sum)
            temp_score = gammaAlphaijk - alphaijkAndSumSijk_sum_lgamma
            temp_score += temptemp
            score += temp_score
            print("the null score is " + str(score))
        return score

    def calculate_score(self, subset_size, top = "all"):
        '''
        A function to calculate BDeuScore

        :param self: instance of BDeuScore class

        :return score: the score
        '''

        feature_list_excepet_target = list(self.dataset_df.columns)

        #print(feature_list_excepet_target)
        feature_list_excepet_target.remove(self.target)
        #print(feature_list_excepet_target)
        subset = self.generate_subset(feature_list_excepet_target, subset_size)
        res = {}
        #print(subset)
        for each_com in subset:
            # print("h")
            # print(each_com)
            dataset_model = Dataset(self.dataset_df, self.target, each_com)
            res[str(each_com)] = self.calculate_score_each_subset(each_com, dataset_model)

        if top == 'all':
            return res
        else:
            return sorted(res.items(), key=lambda item: item[1], reverse=True)[:top]

    def check_if_add(self, curset, threshold = 0.05):
        m = self.m
        target = self.target
        dataset_df = self.dataset_df
        def isExitCase(single_set,single_set_ig,curset,curset_ig):
            set_minus_A = curset[:]
            set_minus_A.remove(single_set[0])
            # print(set_minus_A)
            dataset_model_withoutA = Dataset(dataset_df, target,set_minus_A)
            set_minus_A_ig = self.calculate_informationgain_each_subset(set_minus_A, dataset_model_withoutA) * m
            #set_minus_A_score = self.calculate_score_each_subset(set_minus_A, dataset_model_withoutA) * m
            sum_score = single_set_ig + set_minus_A_ig
            cur_is = (curset_ig - sum_score) / curset_ig
            if cur_is < self.IS:
                self.IS = cur_is
            return cur_is < threshold
        def stillAddable(curset,curset_ig):
            for feature in curset:
                single_set = [feature]
                dataset_model_single = Dataset(dataset_df, target, single_set)
                single_set_ig = self.calculate_informationgain_each_subset(single_set, dataset_model_single) * m
                #single_set_score = self.calculate_score_each_subset(single_set, dataset_model_single) * m
                # calculate the set without the single
                # print(curset)

                if isExitCase(single_set,single_set_ig,curset,curset_ig):
                    return False
            return True
        add = False
        self.IS = 1
        dataset_model = Dataset(self.dataset_df, self.target, curset)
        curset_ig = self.calculate_informationgain_each_subset(curset, dataset_model) * self.m
        #curset_score = self.calculate_score_each_subset(curset, dataset_model) * self.m

        if len(curset) > 1:
            add = stillAddable(curset,curset_ig)
        # is the size of subset is greater than 3, we need to use recursive to break it into all two possible combination

        # if add and len(curset) > 3:
        #     add =
        #I need to use add = recursiveInfoSearch exhaustiveinformationgain 241

        if add:
            self.interaction_strength[str(curset)] = self.IS
        return add


    def calculate_interaction_strength(self, subset_size, threshold = 0.05):
        if subset_size > 1:
            feature_list_excepet_target = list(self.dataset_df.columns)
            feature_list_excepet_target.remove(self.target)
            subsets = self.generate_subset(feature_list_excepet_target, subset_size)
            # print(subsets)
            for subset in subsets:
                self.check_if_add(curset = subset,threshold = threshold)
            return self.interaction_strength

        else:
            print("the subset_size must greater than 2")
            return []



    # {"age":[0,1,3],"race":[0,1,2,3]}
    # we will create one dataset model for each subset
class Search:
    def __init__(self, threshold, max_single_predictors, max_interaction_predictors, max_size_interaction,dataset_input_directory, alpha, target):
        self.dataset_input_directory = dataset_input_directory
        self.alpha = alpha
        self.target = target
        self.threshold = threshold
        self.max_single_predictors = max_single_predictors
        self.max_interaction_predictors = max_interaction_predictors
        self.max_size_interaction = max_size_interaction
        #self.top_interaction_list = collections.OrderedDict()
        self.top_interaction_list = self.get_top_interaction_predictors_score()
        self.top_single_list = self.get_top_singel_predictors_score()

    def get_top_singel_predictors_score(self):
        score = BDeuScore(dataset_input_directory=self.dataset_input_directory, alpha=self.alpha, target=self.target)
        predictors_list = score.dataset_head
        predictors_list.remove(self.target)
        null_score = score.calculate_score(subset_size=0, top="all").values()
        null_score = list(null_score)[0]
        score_dict = score.calculate_score(subset_size=1, top="all")
        single_res = []

        for key,val in score_dict.items():
            if int(val) > null_score:
                single_res.append((key.strip("[]''"),val))
        return single_res

    def get_top_interaction_predictors_score(self):
        interaction_res = {}
        score = BDeuScore(dataset_input_directory=self.dataset_input_directory, alpha=self.alpha, target=self.target)
        #number_of_predictors = score.n
        for i in range(2,self.max_size_interaction + 1):
            cur_infoGain_stren = score.calculate_interaction_strength(subset_size=i,threshold = self.threshold)
            cur_score_dict = score.calculate_score(subset_size=i, top="all")
            for key,val in cur_score_dict.items():
                if key in cur_infoGain_stren:
                    interaction_res[key] = cur_score_dict[key]
        #return Counter(self.top_interaction_list).most_common(1)
        return Counter(interaction_res).most_common(self.max_interaction_predictors)

    def get_new_dataset_after_transform(self):
        def generate_inter_list(interaction):
            interaction = list(interaction[0][1:-1].split(", "))
            new_col = []
            for i in range(score.m):
                new_val = ""
                for item in interaction:
                    item = item.strip("'")
                    new_val += str(score.dataset_df[item][i])

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
        score = BDeuScore(dataset_input_directory=self.dataset_input_directory, alpha=self.alpha, target=self.target)

        #new_dataset = collections.defaultdict(list)
        new_dataset = {}
        for item in self.top_single_list:
            new_col = []
            hash_table = {}
            i = 0
            feature_original_list = list(score.dataset_df[item[0]])
            for val in feature_original_list:
                if val not in hash_table:
                    hash_table[val] = i
                    i += 1
                new_col.append(hash_table[val])
            new_dataset[item[0]] = new_col
        #print(new_dataset)
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
            new_dataset[item[0]] = new_col
        new_dataset[score.target] = list(score.dataset_df[score.target])
        new_status_dataset = generate_new_status_dataset(new_dataset)
        return [new_dataset,new_status_dataset]




        # for item in self.top_interaction_list:
        #     status = item[0]
        #     status = list(status[1:-1].split(", "))
        #     new_status = ""
        #     print(status)
        #     new_list = []
        #     for item in status:
        #         item = item.strip()
        #         new_status += item
        #
        #     print(new_status)
        #

        #     dataset_model = Dataset(score.dataset_df, score.target, status)
        #     subset_status = dataset_model.get_subset_status()
        #     #print(subset_status)
        #     possible_value_list = list(list(subset_status.values()))
        #     possible_value_list.reverse()
        #     #print(possible_value_list)
        #     hash_table = {}
        #     new_col = []
        #     i = 0
        #     for item in itertools.product(*possible_value_list):
        #         val = str(list(reversed(item)))
        #         if val not in hash_table:
        #             hash_table[val] = i
        #             i += 1
        #         new_col.append(hash_table[val])
        #     new_dataset[str(status)] = new_col
        # print(new_dataset)
            # for i in range(len(possible_value_list) -1,-1):


















class Dataset:
    def __init__(self, dataset, target = "E", subset = ["B", "C"]):
        '''
        init function of Dataset class
        :param dataset: the return df from readDataset function
        :param target: the name of the classifier of the model
        :param subset: the name of parent node you want to use in the bayesian network

        '''
        self.number_nodes = dataset.ndim
        self.subset = subset
        self.dataset = dataset
        self.target = target

    def get_target_status(self):
        '''
        A function to get the status of classifier

        :param self: the instance of dataset class

        :return list: A list that include all unique values of classifier
        '''

        return self.dataset[self.target].unique()

    def get_subset_status(self):
        '''
        A function to get the status of the feature in subset

        :param self: the instance of dataset class

        :return map: A map include all unique values of features in subset
        '''
        subset_status_map = defaultdict(list)
        #print(self.subset)
        for item in self.subset:
            item = item.strip("'")
            subset_status_map[item] = self.dataset[item].unique()
        return subset_status_map

    def get_feature_count(self, feature_name):
        '''
        A function to get the count of different feature by feature name

        :param self: the instance of dataset class
        :param feature_name: the name of feature you want to count

        :return Counter: A map that key is the different values for this feature_name and the value is the corresponding count of this value
        '''
        return Counter(self.dataset[self.target])

    def get_parent(self,subset_status_map):
        '''
        A function to get all the possible parent based on the current dataset


        :param self: the instance of dataset class
        :param subset_status_map: a map that the key is the name of current feature and the value is the corresponding unique values of this feature

        :return parent_list:  a list that include all possible parent combinations, when the subset_status_map is {"B":[2,3],"C":[0,1]}, the parent list will be [[0,0], [0,1], [1,0], [1,1]]
        '''
        #defaultdict(<class 'list'>, {'B': array([2, 3], dtype=int64), 'C': array([1, 0], dtype=int64)})
        node_list = list(subset_status_map.values())
        n = len(node_list)
        for i in range(n):
            node_list[i] = list(node_list[i])

        #print(node_list)
        parent_list = list(itertools.product(*node_list))
        #print(parent_list)
        return parent_list

    def get_all_count(self,subset,parent,target_status):
        '''
        A function to get the count of records according to current subset and parent set

        :param self: the instance of dataset class
        :param subset: the current subset like ["B","C"] or ["C","D"]
        :param parent: one of possible parents based on the current subset, if the subset is ["B","C"],B(2,3),C(0,1) the parent list will be [0,0] or [0,1] or [1,0] or [1,1]
        :param target_status: the current target status like "0" or "1"

        :return count: it will be the int the represents how many records you have in the dataset based these conditions
        '''
        select_df = self.dataset
        for i in range(len(subset)):
            select_df = select_df[(select_df[subset[i]] == int(parent[i]))]
        select_df = select_df[(select_df[self.target] == target_status)]
        # subset= [B,C]
        # parent[(2,1)]
        # target_status = 0
        return select_df.shape[0]


    #count = dataset_model.get_all_count(each_com, parent, target_status)

    def get_feature_count_according_target(self,feature_name, feature_value,target_value):
        '''
        A function to get the count of different feature by feature name and feature value


        :param self: the instance of dataset class
        :param feature_name: the name of current feature like "B"
        :param feature_value: one feature name will have different values, for feature "B", it includes "2" or "3"
        :param target_value: the current target value like "0" or "1"

        :return count: it will be the int the represents how many records you have according to the specific condition for the input
        '''
        df2 = self.dataset[(self.dataset[feature_name] == int(feature_value)) & (self.dataset[self.target] == int(target_value))]
        #print(df2)
        return df2.shape[0]

    def get_dataset_size(self):
        return(self.dataset.shape)




# if __name__ == "__main__":
#     #dataset_input_directory = "../datasets/TEST.txt"
#     dataset_input_directory = "../datasets/LSM-15Year.txt"
#     output_directory = "C:/Users/CHX37/Practice"
#     #alpha = 4
#     alpha = 240
#     #target = "E"
#     target = "distant_recurrence"
#     subset_size_list = [0,1,2]
#     top = 20
#     #subset_size_list = [1]
#     #subset_size = 2
#     res1 = {}
#     res2 = {}
#     for subset_size in subset_size_list:
#         score = BDeuScore(dataset_input_directory, alpha, target, subset_size)
#         ir_score = score.calculate_score()
#         res1.update(ir_score)
#         #res1.append(ir_score)
#         ig_score = score.calculate_information_gain()
#         res2.update(ig_score)
#         #res2.append(ig_score)
#     res1_sorted = sorted(res1.items(), key=lambda item: item[1])
#     res2_sorted = sorted(res2.items(), key=lambda item: item[1])
#     print(res1_sorted[:top])
#     print(res2_sorted[:top])





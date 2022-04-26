import math
from collections import defaultdict, Counter
import pandas as pd

class BDeuScore:
    def __init__(self,dataset_model, alpha):
        self.alpha = alpha
        self.dataset_model = dataset_model
        #{"age":[0,1,3],"race":[0,1,2,3]}

        def calculate_score(self):
            subset_status_map = self.dataset_model.get_subset_status()
            target_status_list= self.dataset_model.get_target_status()
            unique_value_count_onefeature_map = self.dataset_model.get_feature_count(self.dataset_model.target)
            score = 0
            # calculate null_score
            if not subset_status_map:
                q = 1
                sijk_sum = 0
                alphaijk = alpha / q
                alphaijkri = alpha / (q * len(target_status_list))
                alphaijk_gamma = math.gamma(alphaijk)
                alphaijkri_gamma = math.gamma(alphaijkri)
                temp_score = 0
                temptemp = 0
                for classifier_value in target_status_list:
                    classifier_count = unique_value_count_onefeature_map[classifier_value]
                    if classifier_count == 0:
                        continue
                    sijk_sum += classifier_count
                    alphaijkri_sum = alphaijkri + classifier_count
                    sumri_gamma = math.gamma(alphaijkri_sum)
                    final_product = sumri_gamma - alphaijkri_gamma
                    temptemp += final_product
                alphaijkAndSumSijk_sum = alphaijk + sijk_sum
                alphaijkAndSumSijk_sum_gamma = math.gamma(alphaijkAndSumSijk_sum)
                temp_score = alphaijk_gamma - alphaijkAndSumSijk_sum_gamma
                temp_score += temptemp
                score += temp_score
                return score



class Dataset:
    def __init__(self, dataset, target, subset):
        self.number_nodes = len(dataset[0])
        self.subset = subset
        self.dataset = dataset
        self.target = target

        def get_target_status(self):
            return self.dataset[self.target].unique()

        def get_subset_status(self):
            subset_status_map = defaultdict(list)
            for item in self.subset:
                subset_status_map[item] = self.dataset[item].unique()
            return subset_status_map

        def get_feature_count(self, feature_name):
            return Counter(self.dataset[self.target])



def readDataset(file, sep='\t'):
    dataset_df = pd.read_csv(file, sep, lineterminator='\n')
    #dataset_df = pd.read_csv(file, sep)
    #dataset_df = dataset_df.iloc[:, :-1]
    print(f'dataset directory: {file}')
    print(f'dataset shape: {dataset_df.shape}')
    print(f'dataset dimension: {dataset_df.ndim}')

    return dataset_df


if __name__ == "__main__":
    input_directory = "C:/Users/CHX37/PycharmProjects/TEST.txt"
    output_directory = "C:/Users/CHX37/Practice"
    dataset = readDataset(input_directory)
    print(dataset)
    alpha = 4
    #target = "distant_recurrence"
    target = "E"
    subset = []
    dataset_model = Dataset(dataset,target,subset)
    score = BDeuScore(dataset_model,alpha)

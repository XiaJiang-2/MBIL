# from abc import ABC, abstractmethod
#
#
# class AbstractClassName(ABC):
#     @abstractmethod
#     def abstract_method_name(self):
#         pass

def calculate_score(self, subset_size, top = "all"):
    '''
    A function to calculate BDeuscore based on subset_size, it will return the score of all possible specific subset with the input subset_size

    :param self: instance of BDeuScore class
    :param subset_size: a int to represent the length of the subset

    :return score: a hash map to store all possible result, the key is the subset and the value is the BDeu score, like{"['B','C']":-3.7534179752515073, "['B','D']":-4.382026634673881,...}
    '''

    feature_list_excepet_target = list(self.dataset_df.columns)

    #print(feature_list_excepet_target)
    feature_list_excepet_target.remove(self.target)
    #print(feature_list_excepet_target)
    subset = self.generate_subset(feature_list_excepet_target, subset_size)
    res = {}
    #print(subset)
    for subset in subset:
        # print("h")
        # print(subset)

        res[str(subset)] = self.BDeu(subset)

    if top == 'all':
        return res
    else:
        return sorted(res.items(), key=lambda item: item[1], reverse=True)[:top]
def calculate_information_gain(self,subset_size,top = "all"):
    '''
    A function to calculate information gain based on subset_size, it will return the score of all possible specific subset with the input subset_size

    :param self: instance of BDeuScore class
    :param subset_size: a int to represent the length of the subset

    :return score: a hash map to store all possible result, the key is the subset and the value is the information score, like{"['B','C']":0.5709505944546684, "['B','D']":0.4199730940219749,...}
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
            score = self.calculate_informationgain_each_subset(each_com)
        res[str(each_com)] = score

    if top == 'all':
        return res
    else:
        return sorted(res.items(), key=lambda item: item[1], reverse=True)[:top]
def generate_subset(self, feature_list, subset_size):
    '''
    A function to generate all possible subset according to the subset_size

    :param feature_list: the list that includes all features in the dataset, it will be ["B", "C", "D", "F"] based on example dataset
    :param subset_size:  the size of the subset you want to generate

    :return list: a list that include all possible subset, if the subset_size == 2, it will be [["B", "C"], ["B", "D"], ["B", "F"], ["C", "D"],["C", "F"], ["D","F"]]
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
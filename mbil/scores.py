class BDeuScore:
    def __init__(self,dataset_df, alpha=4.0, target="E"):
        '''
        init function of BDeuScore class,include functions "generate_subset", "calculate_information_gain", "calculate_score" and so on.

        :param dataset_df: the dataset df you want to use, the return object from ReadDataset class
        :param alpha: A parameter of Bayesian score
        :param target: the name of the target you want to use, the target must be included in dataset

        '''
        self.alpha = alpha
        self.target = target
        self.dataset_df = dataset_df
        self.dataset_head = list(self.dataset_df.columns)
        self.m = self.dataset_df.shape[0]
        self.n = self.dataset_df.shape[1]
        self.interaction_strength = {}
    def BDeu(self, subset):  #Needs to Define a BDeu class instead of a function.
    '''
    A function to calculate BDeuscore for each_subset

    :param subset: the specific subset, like ["B", "C"] or ["B", "D"] based on example dataset

    :return float: the corresponding BDeuscore of this subset
    '''
    dataset_model = Dataset(self.dataset_df, self.target, subset)
    subset_status_map = dataset_model.get_subset_status()
    parent_set = dataset_model.get_parent(subset_status_map)
    target_status_list = dataset_model.get_target_status()
    unique_value_count_onefeature_map = dataset_model.get_feature_count(dataset_model.target)
    score = 0
    # calculate null_score
    if subset:
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
                count = dataset_model.get_all_count(subset, parent, target_status)
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
        # print(str(subset) + " score is " + str(score))
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
        #print("the null score is " + str(score))
    return score

class AIC:
    def __init__(self,dataset_df, alpha=4.0, target="E"):

class IGain:
    def __init__(self,dataset_df, alpha=4.0, target="E"):
        def calculate_informationgain_each_subset(self, subset):
            '''
            A function to calculate information gain for each_subset

            :param subset: the specific subset, like ["B", "C"] or ["B", "D"] based on example dataset

            :return float: the corresponding information gain score of this subset
            '''

            dataset_model = Dataset(self.dataset_df, self.target, subset)
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

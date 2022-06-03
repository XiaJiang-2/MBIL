def BDeu(self, subset):
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
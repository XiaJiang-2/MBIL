# MBIL
MBIL (Markov Blanket and Interactive risk factor learner) is an algorithm that utilizes Bayesian networks and information theory to determine direct and interactive risk factor for metastatic breast cancer (MBC). (See papers for details and citations.)


## Install
MBIL can be installed from PyPI:
`pip install mbil-py`


### For all examples shown:
This is the data:
|B|	C|	D|	F|	E|
|-|--|---|---|---|
|2|	1|	0|	1|	0|
|3|	1|	1|	2|	1|
|3|	0|	1|	1|	0|
|3|	0|	1|	1|	1|
|2|	1|	2|	2|	0|

These are the set parameters:
`alpha = 4`
`target = "E"`
`top = 20`
`max_single_predictors = 20`
`max_interaction_predictors = 20`
`max_size_interaction = 3`
`threshold = 0.05`
`maximum_number_of_parents=7`

These are the basic score and search objects:
`score_test_obj = mbilscore.mbilscore(dataset_df=dataset_df, target=target, alpha=alpha)`

`search_test_object = mbilsearch.mbilsearch(threshold=threshold,
                                           max_single_predictors= max_single_predictors,
                                           max_interaction_predictors=max_interaction_predictors, 
                                           max_size_interaction= max_size_interaction, 
                                           dataset_df = dataset_df, 
                                           alpha = alpha,
                                           target = target)`


## MBILScore functions and their uses:

### mbilscore.calculate_score
Parameters: top and subset_size
Return value: a hashmap storing the results

Calculates the BDeu score for all possible subsets (maybe P(data | DAG))

The BDeu score is a score that measures the probability of the data given the directed acyclic graph using a parameter alpha to represent prior equivalent sample size.

Example:
`scores = score_test_obj.calculate_score(top = top, subset_size = 2)`
`print(scores)`
Output:
`[("['B', 'C']", -3.753417975251508), ("['B', 'F']", -4.158883083359674), ("['B', 'D']", -4.382026634673884), ("['C', 'D']", -4.382026634673884), ("['D', 'F']", -4.382026634673884), ("['C', 'F']", -4.85203026391962)]`


### mbilscore.calculate_information_gain
Parameters: top and subset_size
Return value: a hashmap storing the results

Calculates the information gain for all possible subsets

Information gain is the expected reduction in entropy of a variable conditional on a seperate variable

Example:
`ig_scores = score_test_obj.calculate_information_gain(top = top, subset_size = 2)`
`print(ig_scores)`
Output:
`[("['D', 'F']", 0.5709505944546686), ("['B', 'C']", 0.5709505944546684), ("['B', 'F']", 0.5709505944546684), ("['C', 'D']", 0.5709505944546684), ("['B', 'D']", 0.4199730940219749), ("['C', 'F']", 0.17095059445466854)]`


## MBILSearch functions and their uses:

### mbilsearch.get_single_predictors_score
Parameters: an mbilsearch object
Return value: a list of all direct risk predictors and their corresponding Bayesian score as a float

Calculates the Bayesian score for every direct risk predictor

Example:
When creating an mbilsearch object the function is called when initializing the variable `single_list_score`
Thus the variable can be printed as so
`print(search_test_object.single_list_score)`
Output:
`[('B', -3.5835189384561104)]`

### mbilsearch.get_interaction_predictors_score
Parameters: an mbilsearch object
Return value: a list of the top interactive risk predictors and their corresponding score as a float

Calculates the score between all interactions of predictors

Example:
When creating an mbilsearch object the function is called when initializing the variable `interaction_list_score`
Thus the variable can be printed as so
`print(mbilsearch.interaction_list_score)`
Output:
`[("['B', 'C']", -3.753417975251508), ("['B', 'F']", -4.158883083359674), ("['C', 'D']", -4.382026634673884), ("['D', 'F']", -4.382026634673884), ("['C', 'F']", -4.85203026391962)]`

# MBIL
MBIL (Markov Blanket and Interactive risk factor learner) is an algorithm that utilizes Bayesian networks and information theory to determine direct and interactive risk factor for any appropraite dataset and a given target. (See [papers](https://github.com/XiaJiang-2/MBIL/blob/main/docs/BINF-D-19-00613_R2(2).pdf) for details and citations.)

If anything is unclear in this README, it is highly suggested reading the associated paper.

## Install
MBIL can be installed from PyPI:

`pip install mbil-py`


### For all examples shown:

The data for the examples can be found [here](https://github.com/XiaJiang-2/MBIL/blob/main/datasets/LSM-15Year.txt)

These are the set parameters:

# Add descriptions and ranges for each parameter

`alpha = 4`

alpha is used by the calculate_BDeu function in the scores class and is also known as "equivalent sample size" which is the single hyperparameter when calculating BDeu score. BDeu score calculations are very sensitive to change in this score.

`target = "E"`

Target is the variable that is being determined if any other variables are predictors for.

`top = 20`

Top is the maximum size of the list returned by calculate_score which is called by an mbilscore object.

`max_single_predictors = 20`

Max single predictors is the maximum size of the list returned by get_single_predictors_score.

`max_interaction_predictors = 20`

Max interaction predictors is the maximum size of the list returned by get_interaction_predictors_score.

`max_size_interaction = 3`

Max size interaction is used when determining the maximum size of subsets of interactions between predictors. i.e. 3 would mean the subset could contain 3 predictors ["B", "C", "D"]. 

Note: Using too high of max_size_interaction may cause the program to slow drastically.

`threshold = 0.05`

Threshold is used when calculating interaction strength between predictors to determine whether that interaction is a strong enough interaction to influence the target.

`maximum_number_of_parents=7`

Maximum number of parents is used by the directCause object in the detecting_direct_cause function. It sets the upper limit of the number of direct cause parents for the target.

<br/>

These are the basic direct_cause, score, and search objects:

`direct_cause_obj = mbilsearch.directCause(new_dataset = search_test_object.transformed_dataset, alpha = alpha, target = target, maximum_number_of_parents = maximum_number_of_parents)`

`score_test_obj = mbilscore.mbilscore(dataset_df = dataset_df, target = target, alpha = alpha)`

`search_test_object = mbilsearch.mbilsearch(threshold = threshold, max_single_predictors = max_single_predictors, max_interaction_predictors = max_interaction_predictors, max_size_interaction = max_size_interaction, dataset_df = dataset_df, alpha = alpha, target = target)`


## Functions and Examples

### mbilsearch.get_single_predictors_score

Parameters: The mbilsearch object

Return value: A list of floats with all single predictors whose score is greater than the null score

This function works by taking in the data and parameters set previously and calculates the BDeu score for each predictor and compares it to the null score i.e. if no predictors were present. If the score for said predictor is greater than the null score than it will be added to the list along with its corresponding score.

The BDeu score is a score that measures the probability of the data given the directed acyclic graph using a parameter alpha to represent prior equivalent sample size.

#### Example:

When search_test_object is initialized the single_list_score variable is populated with the list from get_single_predictors_score

`single_list_score = search_test_object.single_list_score`

`print(single_list_score)`

Output:

`[('ethnicity', -522.2549926705351), ('age_at_diagnosis', -523.5126430676971), ('menopause_status', -522.2617336335418), ('t_tnm_stage', -457.84161010478186), ('n_tnm_stage', -206.535586236349), ('stage', -197.65062219483116), ('lymph_node_removed', -334.4424023656752), ('lymph_node_positive', -12.043655034985136), ('size', -475.2257016836076), ('grade', -520.2700620537506), ('invasive', -502.10756560893356), ('histology2', -502.3902665904584), ('invasive_tumor_Location', -517.8283594608185), ('surgical_margins', -522.8691183699473), ('distant_recurrence', -479.8099379450582)]`

![Diagram showing basics of get_single_predictors_score using a directed acyclic graph](MBILProcedure1_img.png)

<br/>

### mbilsearch.get_interaction_predictors_score

Parameters: The mbilsearch object

Return value: A list of floats with all interaction predictors combinations whose score is greater than the null score

This function works by taking in the data and parameters set previously and calculates the interaction strength between parameters. The number of interactions that can occur i.e. 2 predictors, 3 predictors, etc. is set above and will affect the length of computation time

The interaction is calculated via the calculate_interaction_strength function in mbil score and more details on how this value is calculated can be found there.

#### Example:

Similarly to get_single_predictors_score, get_interaction_predictors_score is called when the mbilsearch object is initialized and its value is stored in the interaction_list_score variable.

`interaction_list_score = search_test_object.interaction_list_score`

`print(interaction_list_score)`

Output:

`[("['ER_percent', 'P53', 'n_tnm_stage']", -229.61047654312242), ("['alcohol_useage', 'n_tnm_stage', 'grade']", -247.33107201813266), ("['family_history', 'ER', 'stage']", -251.35598974902388), ("['family_history', 'ER_percent', 'stage']", -267.55001937152036), ("['family_history', 'PR_percent', 'stage']", -272.0735376165017), ("['family_history', 'PR', 'stage']", -273.84770197402185), ("['alcohol_useage', 'family_history', 'stage']", -283.65802337173835), ("['alcohol_useage', 'family_history', 'n_tnm_stage']", -307.3724355739906), ("['alcohol_useage', 'n_tnm_stage', 'DCIS_level']", -312.3468295757039), ("['ER', 'lymph_node_removed', 'surgical_margins']", -361.93119355717835), ("['smoking', 'side', 'lymph_node_removed']", -362.59608464332837), ("['family_history', 'n_tnm_stage', 'DCIS_level']", -380.1096531444613), ("['family_history', 'TNEG', 'lymph_node_removed']", -393.01803294278534), ("['family_history', 'lymph_node_removed', 'surgical_margins']", -397.2146085038911), ("['family_history', 'ER', 'lymph_node_removed']", -412.57095239825867), ("['family_history', 'ER_percent', 'lymph_node_removed']", -415.1720042660745), ("['age_at_diagnosis', 'lymph_node_removed', 'DCIS_level']", -418.508108825582), ("['family_history', 'age_at_diagnosis', 'lymph_node_removed']", -420.123897008576), ("['ER', 'lymph_node_removed', 'DCIS_level']", -420.283759150574), ("['lymph_node_removed', 'DCIS_level', 'surgical_margins']", -421.43289368440406)]`

![Diagram showing basics of get_interaction_predictors_score using a directed acyclic graph](ExampleOfInteractiveModels2022.8.png)

<br/>

### directCause.detecting_direct_cause

Parameters: The directCause object

Return value: a list of predictors that are a direct cause according to the parent list

This function works by taking in the data and parameters set previously and calculates what single predictors and interactive predictors can be considered direct causes of the target.

#### Example:

As with the other functions, this function is called when a directCause object is initialized and its return value is stored in the direc_cause variable.

`print(direct_cause_obj.direc_cause)`

Output:

`['lymph_node_positive']`




# MBIL
MBIL (Markov Blanket and Interactive risk factor learner) is an algorithm that utilizes Bayesian networks and information theory to determine direct and interactive risk factor for any appropraite dataset and a given target. (See [papers](https://github.com/XiaJiang-2/MBIL/blob/main/docs/BINF-D-19-00613_R2(2).pdf) for details and citations.)

If anything is unclear in this README, it is highly suggested reading the associated paper.

## Install
MBIL can be installed from PyPI:

`pip install mbil-py`


### For all examples shown:

The data for the examples can be found [here](https://github.com/XiaJiang-2/MBIL/blob/main/datasets/LSM-15Year.txt)

These are the set parameters:

`alpha = 4`

Alpha is used by the calculate_BDeu function in the scores class and is also known as "equivalent sample size" which is the single hyperparameter when calculating BDeu score. BDeu score calculations are very sensitive to change in this score.

`target = "distant_recurrence"`

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

`[('race', -369.8452513792026), ('ethnicity', -366.3669802964773), ('age_at_diagnosis', -367.5144230392912), ('menopause_status', -369.598618296
166), ('TNEG', -366.9731301525993), ('ER', -367.3621787201608), ('ER_percent', -367.65151978822803), ('PR', -368.252751312568), ('PR_percent',
-368.0831950555779), ('P53', -368.365568684018), ('t_tnm_stage', -335.0582136785349), ('n_tnm_stage', -334.48015803286694), ('stage', -329.3514
061061729), ('lymph_node_removed', -347.8555475785), ('lymph_node_positive', -327.0591540402502), ('lymph_node_status', -325.5865849226134), ('
size', -344.0126639909387), ('grade', -354.9715104823545), ('invasive', -358.57524130106475), ('histology2', -361.492396116718), ('invasive_tum
or_Location', -366.060734143025), ('re_excision', -369.4534986096347), ('surgical_margins', -367.9622319094127), ('MRIs_60_surgery', -369.27100
94976411)]`

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

`[("['age_at_diagnosis', 'menopause_status', 'lymph_node_status']", -316.57958315640474), ("['ER_percent', 'lymph_node_status']", -323.166074516
6482), ("['age_at_diagnosis', 'lymph_node_status']", -323.38591931843985), ("['ER', 'lymph_node_status']", -323.6624329636214), ("['age_at_diag
nosis', 'menopause_status', 'lymph_node_positive']", -325.2652703071466), ("['ER', 'lymph_node_positive']", -327.3258554505689), ("['age_at_dia
gnosis', 'lymph_node_positive']", -327.3611930742304), ("['ER_percent', 'lymph_node_positive']", -327.397677955001), ("['age_at_diagnosis', 'ly
mph_node_status', 'grade']", -328.3330212115378), ("['age_at_diagnosis', 'TNEG', 'lymph_node_status']", -329.41650396548073), ("['age_at_diagno
sis', 'lymph_node_status', 're_excision']", -330.54880597511806), ("['alcohol_useage', 'lymph_node_status']", -330.9462428049852), ("['PR_perce
nt', 'lymph_node_positive']", -331.7820953526888), ("['n_tnm_stage', 'surgical_margins']", -331.94349696591223), ("['TNEG', 'lymph_node_positiv
e', 're_excision']", -332.3535728487969), ("['ER', 'HER2', 'lymph_node_status']", -333.0770426415594), ("['lymph_node_status', 'Histology', 'in
vasive_tumor_Location']", -333.0961085924088), ("['ethnicity', 'TNEG', 'stage']", -333.1903385140786), ("['age_at_diagnosis', 'stage']", -333.4
8963390421807), ("['age_at_diagnosis', 'ER_percent', 'lymph_node_status']", -333.8132984731466)]`

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

`["['age_at_diagnosis', 'menopause_status', 'lymph_node_status']"]`




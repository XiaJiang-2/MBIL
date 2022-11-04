# MBIL
MBIL (Markov Blanket and Interactive risk factor Learner) is an algorithm designed to detect and learn the risk factors  . (See [papers](https://github.com/XiaJiang-2/MBIL/blob/main/docs/BINF-D-19-00613_R2(2).pdf) for details and citations.)
# please explain what is MBIL using your own words and be complete and accurate. For example, you need to say what theory BMIL is based.

## Explain how to use MBIL Algorithm (functions) by creating example datasets and use cases... 

![MBILProcedure1_img.png](MBILProcedure1_img.png)
## Installation
MBIL can be installed from [PyPI](https://pypi.org/project/mbil-py/)


```py
pip install mbil-py
```
#test the installation procedure and see if it works. If not, write about the correct way to install. 
##  Importing Libraries

'''py
import mbil
from mbil import dataset
from mbil import scores
from mbil import mbilsearch
from mbil import output
'''

##  Input Settings
#These copy and past stuff are not good for explaining how MBIL can be used. 
```py
alpha = 4   #set the desired value of alpha
target = "E"    #Target featureset
top = 20
max_single_predictors = 20  
max_interaction_predictors = 20
max_size_interaction = 3
threshold = 0.05
maximum_number_of_parents = 7 #Maximum parents of the featureset
```

##  Creating a Search Object

```py
search_test_obj = mbilsearch.mbilsearch(threshold=threshold,
                                           max_single_predictors= max_single_predictors,
                                           max_interaction_predictors=max_interaction_predictors,
                                           max_size_interaction= max_size_interaction,
                                           dataset_df = dataset_df,
                                           alpha = alpha,
                                           target = target)
```

##  Object to find the Direct Cause using MBIL Search

```py
direct_cause_obj = mbilsearch.directCause(
    new_dataset = search_test_obj.transformed_dataset,
    alpha= alpha,
    target = target,
    maximum_number_of_parents = maximum_number_of_parents)
```

##  Creating Output Object

```py
output_path = "output/" #Output stored in the output folder
dataset_name = "Test"   #Name can be anything according to the predfined dataset
all_input_hash_map = {"alpha": alpha,
                      "target":target, 
                      "top":top, 
                      "max_single_predictors":max_single_predictors, 
                      "max_interaction_predictors":max_interaction_predictors,
                      "max_size_interaction":max_size_interaction, 
                      "threshold":threshold, 
                      "maximum_number_of_parents":maximum_number_of_parents}

number_of_predictors = dataset_df.shape[1] - 1
number_of_records = dataset_df.shape[0]
dataset_information = {"number_of_predictors":number_of_predictors, "number_of_records":number_of_records}

output_obj = output.output(
                           output_path = output_path,
                           dataset_name = dataset_name , 
                           all_input = all_input_hash_map, 
                           dataset_path = dataset_input_directory, 
                           dataset_information = dataset_information, 
                           null_score = score_test_obj.calculate_score(top = top, subset_size = 0), 
                           single_score = search_test_obj.single_list_score, 
                           interaction_score = search_test_obj.interaction_list_score, 
                           direc_cause = direct_cause_obj.direc_cause)
```

##  MBILScore - functions and variables

mbilscore.mbilscore function is used to calculate the MBIL Score according ot the input dataset.

### calculate_score(top = top, subset_size = "Required subset size")

```py
null_score = score_test_obj.calculate_score(top = top, subset_size = 0)
```
### calculate_information_gain(top = top, subset_size = "Required subset size")

```py
null_information_gain = score_test_obj.calculate_information_gain(top = top, subset_size = 0)
```

### Different Subsets give different results - the plot below can help identify the differences.

```py
score_test_obj.plot_score(subset_size = 1)
```
[C:\Users\dhruv\MBIL\score_plot.png](score_plot.png)

```py
score_test_obj.plot_score(subset_size = 2)
```
[C:\Users\dhruv\MBIL\score_plot2.png](../../score_plot2.png)

### Bar Graph with the result of Information Gain
```py
score_test_obj.plot_information_gain(subset_size = 1)
```
[Information_gain.png](../../IG_result.png)

```py
score_test_obj.plot_information_gain(subset_size = 2)
```
[IG_result2.png](../../IG_result2.png)


##  Functions of MBILSearch

mbilSearch was used to find the strong single predictors and interaction predictors according to the threshold.

```py
search_test_obj = mbilsearch.mbilsearch(threshold=threshold,
                                           max_single_predictors= max_single_predictors,
                                           max_interaction_predictors=max_interaction_predictors,
                                           max_size_interaction= max_size_interaction,
                                           dataset_df = dataset_df,
                                           alpha = alpha,
                                           target = target)
```

### Print single_pedictor list after search

```py
single_list = search_test_obj.single_list_score
```

### Print interaction_predictor list after search

```py
interactions_list = search_test_obj.interaction_list_score
```

### Print transformed dataset

```py
search_test_obj.transformed_dataset
```

### Plot bar gragh of the final score result

```py
search_test_obj.plot_score_aftersearch()
```
[final_score.png](../../final_score.png)
## Main Classes Introduction
1. mbilscore.mbilScore: mbilScore was used to calculate the mbImilScore according to the input dataset.

2. mbilsearch.mbilSearch: mbilSearch was used to find the strong single predictors and interaction predictors according to the threshold.

3. mbilsearch.directCause: directCause was used to out put the final direct cause after the mbil search.

4. scores.BDeuScore: BDeuScore was used to finish the basic calculation work about BDeuScore.

5. scores.IGain: IGain was used to finish the basic calculation work about IGain.

6. output.output: output was used to output the log and important result of the mbil search

## How to use mbil package and specific example
![img_7.png](img_7.png)





Example of BDeu Score
Chuhan finish

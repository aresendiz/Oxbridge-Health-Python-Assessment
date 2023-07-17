"""
Python Screening Test for Oxbridge Health: Problem 1
Developed by: Angelica Resendiz
On: 7/12/2023
With: Python 3.9.12, Pandas 1.4.3
Limitations: Function superset_check uses itertuples, a list-valued key 
              won't work since list are non hashable. This part could be done
              with a outer merge if list-valued keys can be added
Assumptions: The merge key of the left dataset is always chosen, even
             when neither dataframe is a superset of the other. A different
             approach can be done where no columns are drop on this case.

             The merge key type comparison is done on pd.merge(), no extra functionality
             was added

             Auxiliarly functions were created for readibility reasons
"""
import pandas as pd
import numpy as np

def superset_check(df1, df2, on_left, on_right, superset):

    df1_set = set(df1[on_left].itertuples(index = False, name = None))
    df2_set = set(df2[on_right].itertuples(index = False, name = None)) 
    
    df1_superset = df2_set.issubset(df1_set)
    df2_superset = df1_set.issubset(df2_set)
    equal = df1_set == df2_set

    if superset == 'left' and not df1_superset :
        raise Exception("The left data frame is not a superset")
    
    if superset == 'right' and not df2_superset:
        raise Exception("The right data frame is not a superset")
    
    if superset == 'all' and not equal:
        raise Exception("The data frames don't contain the same set of merge key combinations")
    
    return df1_superset, df2_superset
    
def key_processing(df1, df2, on=None, left_on=None, right_on=None):
    
    if left_on is None and right_on  is None and on is None :
        left_on = df1.columns.values.tolist()
        right_on = df2.columns.values.tolist()
    
    elif on is not None: 
        left_on = on
        right_on = on

    left_on = [left_on] if isinstance(left_on, str) else left_on
    right_on = [right_on] if isinstance(right_on, str) else right_on

    return left_on, right_on

def select_merge_columns (df,left_on, right_on, df1_superset, df2_superset):

    if df1_superset:
        df.drop(columns = right_on, inplace = True)
    elif df2_superset:
        df.drop(columns = left_on, inplace = True)
    else:
        for column_left, column_right  in zip(left_on, right_on):
            df[column_left] = np.where(df['ind'] == 'right_only', df[column_right],df[column_left])
        df.drop(columns = right_on, inplace = True)
    
    return df

def enhanced_merge(df1, df2, validate, superset = None, on=None, left_on=None, right_on=None, indicator=False, matched_obs = False, *args,**kwargs):
    ## Extra Functionality 1: Optional superset check
    if superset is not None and superset not in ['left', 'right', 'all']: 
        raise ValueError(f'{superset} is not a valid argument for superset')
    
    left_on, right_on = key_processing(df1, df2, on, left_on, right_on)

    df1_superset, df2_superset = superset_check(df1, df2, left_on, right_on, superset)
    
    ### Extra Functionality 3: Check merge columns Types
    ### Already part of merge
     
    ########
    df = pd.merge(df1,df2, validate = validate, on = on, left_on = left_on, right_on = right_on, indicator = 'ind', *args, **kwargs)

    ### Extra Functionality 4: No matched observations
    if matched_obs == True and 'both' not in  df['ind'].unique():
        raise Exception("No Matched Observations")

    ### Extra Functionality 2: Drop set of merge columns when left_on != right_on
    if left_on != right_on:
        df = select_merge_columns (df,left_on, right_on, df1_superset, df2_superset)
     
    ########
    if indicator == False: # remove indicator or rename
        df.drop(columns = ['ind'], inplace = True)
    else:
        df.rename(columns={'ind': indicator}, inplace = True)
    
    return df

#######################################################
####### Tests Cases ###################################
#######################################################

left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'], 
                 'key2': ['K0', 'K1', 'K0', 'K0'],
                 'A': ['A0', 'A1', 'A2', 'A3'],
                 'B': ['B0', 'B1', 'B2', 'B3']})

right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                      'key2': ['K0', 'K0', 'K0', 'K0'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3'],
                      'E': [1,2,3,4]})

right2 = pd.DataFrame({'keys1': ['K0', 'K1', 'K1', 'K2'],
                      'keys2': ['f', 'f0', 'f0', 'f0'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3'],
                      'E': [1,2,3,4]})

### Test 1: Optional superset check
print ('Test 1: Checks that the right dataframe contains a superset of merge key combinations available in the left dataset.')
try:
    print(enhanced_merge(left, right, validate = '1:m', left_on=['key1','key2'], right_on=['key1','key2'], how='outer', superset = 'right'))
except:
    print('An error was raised since the dataframe is not a superset')
finally:
    print("Now, let's see if the dataframe contains a superset of merge key combinations available in the right dataset")

try:
    print(enhanced_merge(left, right, validate = '1:m', left_on=['key1','key2'], right_on=['key1','key2'], how='outer', superset = 'left'))
except:
    print('An error was raised since the dataframe is not a superset')
finally:
    print('The merged dataframe was produced')

### Test 2: Single set of key columns
print ('Test 2: The resulting merged dataset contain a single set of key columns when specifying different sets of columns for left_on and right_on,.')
print("These are the left frame keys: ['key1','key2'], and the right frame keys: ['keys1','keys2']")
print(enhanced_merge(left, right2, validate = '1:m', left_on=['key1','key2'], right_on=['keys1','keys2'], how='outer'))

### Test 3: No matched observations
print ('Test 3: Checks that no matched observations from the two input datasets in the resulting dataset')
try:
    print(enhanced_merge(left, right2, validate = '1:m', left_on=['key1','key2'], right_on=['keys1','keys2'], how='outer', superset = 'right', matched_obs = True ))
except:
    print('An error was raised since there are no matched observations')

### Test 4: Validate is a required argument
print ('Test 4: Checks that Validate is a required argument')
try:
    print(enhanced_merge(left, right2, left_on=['key1','key2'], right_on=['keys1','keys2'], how='outer', superset = 'right', matched_obs = True ))
except:
    print('An error was raised since Validate is a required argument')

### Test 5: Check merge columns across the left and right dataframe for consistency of their types 
print ('Test 5: Check merge columns across the left and right dataframe for consistency of their types.')
try:
    print(enhanced_merge(left, right2, validate = '1:m', left_on=['key1','key2'], right_on=['keys1','E'], how='outer', superset = 'right', matched_obs = True ))
except:
    print('An error was raised beacause of type inconsistencies')




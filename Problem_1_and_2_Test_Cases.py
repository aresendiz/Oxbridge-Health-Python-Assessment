"""
Python Screening Test for Oxbridge Health: Test Cases for Problem 1 and 2
Developed by: Angelica Resendiz
On: 7/12/2023
With: Python 3.9.12, Pandas 1.4.3

"""
import Problem_1 as pm1
import Problem_2 as pm2
import pandas as pd

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
    print(pm1.enhanced_merge(left, right, validate = '1:m', left_on=['key1','key2'], right_on=['key1','key2'], how='outer', superset = 'right'))
except:
    print('An error was raised since the dataframe is not a superset')
finally:
    print("Now, let's see if the dataframe contains a superset of merge key combinations available in the right dataset")

try:
    print(pm1.enhanced_merge(left, right, validate = '1:m', left_on=['key1','key2'], right_on=['key1','key2'], how='outer', superset = 'left'))
except:
    print('An error was raised since the dataframe is not a superset')
finally:
    print('The merged dataframe was produced')

### Test 2: Single set of key columns
print ('Test 2: The resulting merged dataset contain a single set of key columns when specifying different sets of columns for left_on and right_on,.')
print("These are the left frame keys: ['key1','key2'], and the right frame keys: ['keys1','keys2']")
print(pm1.enhanced_merge(left, right2, validate = '1:m', left_on=['key1','key2'], right_on=['keys1','keys2'], how='outer'))

### Test 3: No matched observations
print ('Test 3: Checks that no matched observations from the two input datasets in the resulting dataset')
try:
    print(pm1.enhanced_merge(left, right2, validate = '1:m', left_on=['key1','key2'], right_on=['keys1','keys2'], how='outer', superset = 'right', matched_obs = True ))
except:
    print('An error was raised since there are no matched observations')

### Test 4: Validate is a required argument
print ('Test 4: Checks that Validate is a required argument')
try:
    print(pm1.enhanced_merge(left, right2, validate = '1:m', left_on=['key1','key2'], right_on=['keys1','keys2'], how='outer', superset = 'right', matched_obs = True ))
except:
    print('An error was raised since Validate is a required argument')

### Test 5: Check merge columns across the left and right dataframe for consistency of their types 
print ('Test 5: Check merge columns across the left and right dataframe for consistency of their types.')
try:
    print(pm1.enhanced_merge(left, right2, validate = '1:m', left_on=['key1','key2'], right_on=['keys1','E'], how='outer', superset = 'right', matched_obs = True ))
except:
    print('An error was raised beacause of type inconsistencies')



#### Test case

df = pd.DataFrame({'event_1_start_date': pd.date_range(start='2021-08-03', end='2021-11-01', freq='W'), 
                    'event_1_end_date': pd.date_range(start='2021-11-03', end='2022-02-01', freq='W'),
                    'event_2_start_date': pd.date_range(start='2021-11-16', periods=13, freq="D"),
                    'event_2_end_date': pd.date_range(start='2022-11-13', periods=13, freq="w")
                    }
    )

df['diff'] = pm2.days_of_overlap(df,'event_1_start_date', 'event_1_end_date','event_2_start_date','event_2_end_date')

print(df)
    

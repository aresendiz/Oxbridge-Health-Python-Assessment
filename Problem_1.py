"""
Python Screening Test for Oxbridge Health: Problem 1
Developed by: Angelica Resendiz
On: 7/12/2023
With: Python 3.9.12, Pandas 1.4.3
Limitations: Function validate_superset uses itertuples, a list-valued key 
              won't work since list are non hashable. This part could be done
              with a outer merge if list-valued keys can be added
Assumptions: The merge key of the left dataset is always chosen, even
             when neither dataframe is a superset of the other. A different
             approach can be done where no columns are drop on this case.

             The merge key type comparison is done on pd.merge(), no extra functionality
             was added

Notes: The problem was initially solved breaking up the enhanced_merge function into
auxiliarly functions. Finally a class approach was implemented to utilized cache property 
"""

import pandas as pd
import numpy as np
from functools import cached_property

class EnhancedMerger:
    def __init__(
        self,
        df1,
        df2,
        validate,
        superset=None,
        on=None,
        left_on=None,
        right_on=None,
        indicator=False,
        matched_obs=False,
    ):
        self._df1 = df1
        self._df2 = df2
        self._validate = validate
        self._superset = superset
        self._on = on
        self._left_on = left_on
        self._right_on = right_on
        self._indicator = indicator
        self._matched_obs = matched_obs

        self._process_merge_keys()

        self._validate_superset()

    def _process_merge_keys(self):
        if self._on is not None: 
            self._left_on = self._on
            self._right_on = self._on

        self._left_on = [self._left_on] if isinstance(self._left_on, str) else self._left_on
        self._right_on = [self._right_on] if isinstance(self._right_on, str) else self._right_on

    @cached_property
    def _df1_is_superset(self):
        df1_set = set(self._df1[self._left_on].itertuples(index = False, name = None))
        df2_set = set(self._df2[self._right_on].itertuples(index = False, name = None)) 

        return df2_set.issubset(df1_set)
    
    @cached_property
    def _df2_is_superset(self):
        df1_set = set(self._df1[self._left_on].itertuples(index = False, name = None))
        df2_set = set(self._df2[self._right_on].itertuples(index = False, name = None)) 

        return df1_set.issubset(df2_set)

    def _validate_superset(self): ### Extra Functionality: Validate supercheck
        if self._superset is not None and self._superset not in ['left', 'right', 'all']: 
            raise ValueError(f'{self._superset} is not a valid argument for superset')
        
        if self._superset is not None and self._on is None and self._left_on is None:
            raise ValueError('No merge columns were specified')

        if self._superset == 'left' and not self._df1_is_superset :
            raise Exception("The left data frame is not a superset")
        
        if self._superset == 'right' and not self._df2_is_superset:
            raise Exception("The right data frame is not a superset")
        
        if self._superset == 'all' and not (self._df2_is_superset and self._df1_is_superset):
            raise Exception("The data frames don't contain the same set of merge key combinations")

    def _select_merge_columns(self, df):
        if self._df1_is_superset:
            df.drop(columns = self._right_on, inplace = True)
        elif self._df2_is_superset:
            df.drop(columns = self._left_on, inplace = True)
        else:
            for column_left, column_right  in zip(self._left_on, self._right_on):
                df[column_left] = np.where(df['ind'] == 'right_only', df[column_right],df[column_left])
            df.drop(columns = self._right_on, inplace = True)
        
        return df

    def merge(self, *args, **kwargs):
        df = pd.merge(
                    self._df1,
                    self._df2,
                    validate = self._validate, 
                    left_on = self._left_on, 
                    right_on = self._right_on, 
                    indicator = 'ind', 
                    *args, 
                    **kwargs)

        ### Extra Functionality 4: No matched observations
        if self._matched_obs and 'both' not in  df['ind'].unique():
            raise Exception("No Matched Observations")

        ### Extra Functionality 2: Drop set of merge columns when left_on != right_on
        if self._left_on != self._right_on:
            df = self._select_merge_columns(df)
        
        ########
        if self._indicator == False: # remove indicator or rename
            df.drop(columns = ['ind'], inplace = True)
        else:
            df.rename(columns={'ind': self._indicator}, inplace = True)
        
        return df


def enhanced_merge(
    df1, 
    df2, 
    validate, 
    left_on=None, 
    right_on=None, 
    superset=None, 
    on=None, 
    indicator=False, 
    *args, 
    **kwargs,
):
    enhanced_merger = EnhancedMerger(
        df1, 
        df2, 
        validate, 
        left_on=left_on, 
        superset=superset, 
        on=on,
        right_on=right_on, 
        indicator=indicator,
    )
    return enhanced_merger.merge(*args, **kwargs)



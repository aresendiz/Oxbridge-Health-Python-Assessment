"""
Python Screening Test for Oxbridge Health: Problem 2
Developed by: Angelica Resendiz
On: 7/12/2023
With: Python 3.9.12, Pandas 1.4.3
Limitations: The function doesn't check that start_date is before than end_date
             The function doesn't check for nulls
             Data preprocessing will be necessry
Assumptions: The start_date, end_date intervals are considered closed intervals, e.g.,
                If event_1 ends on date_1 and event_2 starts on date_1, date_1 is counted
                as an overlapping day
"""
import pandas as pd
import numpy as np

def days_of_overlap(df):
    
    df['diff'] = (df[['event_1_end_date','event_2_end_date']].min(axis=1) -
                df[['event_1_start_date','event_2_start_date']].max(axis=1)).dt.days + 1

    df['diff'] = np.where(df['diff'] > 0, df['diff'], 0)

    return df

#### Test case

df = pd.DataFrame({'event_1_start_date': pd.date_range(start='2021-08-03', end='2021-11-01', freq='W'), 
                  'event_1_end_date': pd.date_range(start='2021-11-03', end='2022-02-01', freq='W'),
                  'event_2_start_date': pd.date_range(start='2021-11-16', periods=13, freq="D"),
                  'event_2_end_date': pd.date_range(start='2022-11-13', periods=13, freq="w")
                  }
)

print(days_of_overlap(df))
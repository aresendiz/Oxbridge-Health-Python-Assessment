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

def days_of_overlap(df,event_1_start_date, event_1_end_date,event_2_start_date,event_2_end_date):
    
    diff = (df[[event_1_end_date,event_2_end_date]].min(axis=1) -
                df[[event_1_start_date,event_2_start_date]].max(axis=1)).dt.days + 1

    diff = np.where(diff > 0, diff, 0)

    return diff






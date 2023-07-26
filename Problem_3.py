"""
Python Screening Test for Oxbridge Health: Problem 2
Developed by: Angelica Resendiz
On: 7/12/2023
With: Python 3.9.12, Pandas 1.4.3

"""
import pandas as pd
import Problem_2 as pm2

medical_events = pd.read_excel('all_test_data_2023_06_29.xlsx', sheet_name='medical_events')

enrollment = pd.read_excel('all_test_data_2023_06_29.xlsx', sheet_name='enrollment') 

death_rates = pd.read_excel('all_test_data_2023_06_29.xlsx', sheet_name='death_dates') 

########## flatten enrollment ##############

#Convert to datetime to sort values
enrollment['enrollment_start'] = pd.to_datetime(enrollment['enrollment_start_year_month'])

enrollment['enrollment_end'] = pd.to_datetime(enrollment['enrollment_end_year_month'])

enrollment = enrollment.sort_values(['patient_id', 'enrollment_start', 'enrollment_end'])

# adds 1 everytime there is a gap, creating a new group
enrollment['enrollment_group'] = (enrollment['enrollment_start'] > 
                                    enrollment.groupby(['patient_id'])['enrollment_end'].shift()
                                 ).groupby([enrollment['patient_id']]).cumsum()

# group by patient id and enrollment group 
enrollment = enrollment.groupby(['patient_id', 'enrollment_group'], as_index=False
                                ).aggregate({'enrollment_start': 'min', 'enrollment_end': 'max'})

# merge enrollment with death date

enrollment = pd.merge(enrollment, death_rates, on = 'patient_id', how='left', validate='m:1'
                      ).fillna(pd.to_datetime("2110-01-01"))
enrollment['end_date'] = enrollment[['enrollment_end','death_date']].min(axis=1)
enrollment.drop(columns = ['enrollment_end','death_date'], inplace=True)
 
# Compare number of day on event vs number of days in overlap

enrollment = pd.merge(enrollment, medical_events, on = 'patient_id', how='left', validate='m:m')

enrollment['overlap_days']=pm2.days_of_overlap(enrollment,'enrollment_start', 'end_date',
                                               'even_start_date','event_end_date')

enrollment['event_days']=(enrollment['event_end_date'] - enrollment['even_start_date']).dt.days +1

print(enrollment.loc[enrollment['overlap_days'] == enrollment['event_days'], 
                     ['patient_id', 'enrollment_group', 'event_id']])


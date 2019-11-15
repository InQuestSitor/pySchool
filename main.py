# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 21:23:16 2019

@author: aregh
"""

# Import the required modules
import pandas as pd
import statistics as st

# Import the datasets to be analysed
sch = pd.read_csv('schools_complete.csv') 
std = pd.read_csv('students_complete.csv')

### District Summary
# Create a high level snapshot (in table form) of the district's key metrics:

def district_summary(x,y):
    sch_ttl = x['school_name'].count()                          # Total Schools
    std_ttl = x['size'].sum()                                   # Total Students
    ttl_bdg = x['budget'].sum()                                 # Total Budget
    av_math = y['math_score'].mean()                            # Average Math Score
    av_read = y['reading_score'].mean()                         # Average Reading Score
    nb_math = y['math_score'].count()                           # Total Math Students
    nb_read = y['reading_score'].count()                        # Total Reading Students
    
    # Let's say the pass score is 70 and above, the number of Math and Reading with pass score:
    ps_math = (y['math_score']>=70).sum()
    ps_read = (y['reading_score']>=70).sum()
    
    # % of students passing Math and Reading:
    pt_math = ps_math / nb_math * 100                           # % Passing Math
    pt_read = ps_read / nb_read * 100                           # % Passing Reading
    ov_pass = st.mean([pt_math, pt_read])                       # Overall Passing Rate (Average of the Math and Reading pass rate)
    
    ## Create a high level snapshot (in table form) of the district's key metrics
    # Create and iput the computed metrics into a dataframe:
    df = pd.DataFrame([sch_ttl, std_ttl, ttl_bdg, 
                       f'{round(av_math,2)}', f'{round(av_read,2)}', 
                       f'{round(pt_math,2)}%', f'{round(pt_read,2)}%', 
                       f'{round(ov_pass,2)}%'], index=['Total Schools', 
                          'Total Students', 'Total Budget','Average Math Score', 
                          'Average Reading Score', '% Passing Math', 
                          '% Passing Reading', 'Overall Passing Rate'], 
    columns=['Key Metrics'])
    print ('District Summary')
    print ('-'*len('District Summary'))
    return df

### School Summary
# Create an overview table that summarizes key metrics about each school:

# Calculate PerStudentBudget by dividing individual school budget by its (student) size.:
def per_std_bdgt(x,y):
    return x/y

def school_metrics(x):
    group_name = std.groupby('school_name')
    hs = group_name.get_group(x)
    return hs
    
def avg_math_score(x):
    hs = school_metrics(x)
    hs_av_math = hs['math_score'].mean()                          # School Average Math Score
    return round(hs_av_math,2)

def avg_read_score(x):
    hs = school_metrics(x)
    hs_av_read = hs['reading_score'].mean()                       # School Average Reading Score
    return round(hs_av_read,2)

    # % of School students passing Math and Reading:
    # Let's say the pass score is 70 and above, the number of Math and Reading with pass score:
def pct_pass_math(x):
    hs = school_metrics(x)    
    hs_nb_math = hs['math_score'].count()                         # School Total Math Students
    hs_ps_math = (hs['math_score']>=70).sum()
    hs_pt_math = hs_ps_math / hs_nb_math * 100                    # % Passing Math
    return round(hs_pt_math,2)

def pct_pass_read(x):
    hs = school_metrics(x)    
    hs_nb_read = hs['reading_score'].count()                      # School Total Reading Students
    hs_ps_read = (hs['reading_score']>=70).sum()
    hs_pt_read = hs_ps_read / hs_nb_read * 100                    # % Passing Reading
    return round(hs_pt_read,2)
    
def over_pass_rate(x):
    return st.mean([pct_pass_math(x), pct_pass_read(x)])          # Overall Passing Rate (Average of the Math and Reading pass rate)
      

### District Summary
print(district_summary(sch,std))

### School Summary
sch['Per Student Budget']=[per_std_bdgt(x,y) for x, y in zip(sch['budget'], 
   sch['size'])]
sch['Average Math Score'] = [avg_math_score(x) for x in sch['school_name']]
sch['Average Reading Score'] = [avg_read_score(x) for x in sch['school_name']]
sch['% Passing Math'] = [f'{pct_pass_math(x)}%' for x in sch['school_name']]
sch['% Passing Reading'] = [f'{pct_pass_read(x)}%' for x in sch['school_name']]
sch['Overall Passing Rate'] = [over_pass_rate(x) for x in sch['school_name']]
    
print ('School Summary')
print ('-'*len('School Summary'))
print (sch.drop(['School ID'], axis=1).set_index('school_name'))

### Top Performing Schools (By Passing Rate)
# Create a table that highlights the top 5 performing schools based on Overall Passing Rate.
nnn = sch.drop(['School ID'], axis=1).set_index('school_name')
print ('Top Performing Schools (By Passing Rate)')
print ('-'*len('Top Performing Schools (By Passing Rate)'))
print (nnn.sort_values(by=['Overall Passing Rate'], ascending=False).head(5))

### Bottom Performing Schools (By Passing Rate)
# Create a table that highlights the bottom 5 performing schools based on Overall Passing Rate. 
nnn = sch.drop(['School ID'], axis=1).set_index('school_name')
print ('Bottom Performing Schools (By Passing Rate)')
print ('-'*len('Bottom Performing Schools (By Passing Rate)'))
print (nnn.sort_values(by=['Overall Passing Rate'], ascending=True).head(5))

### Math Scores by Grade
# Create a table that lists the average Math Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
mgs = std.groupby(['grade','school_name'])['math_score']
avg_mgs = pd.DataFrame(round(mgs.mean(),2))
mg = pd.concat([avg_mgs.loc['9th'], avg_mgs.loc['10th'], avg_mgs.loc['11th'], 
                avg_mgs.loc['12th']], axis=1, keys=['9th grade','10th grade',
                           '11th grade','12th grade'])
print ('Math Scores by Grade')
print ('-'*len('Math Scores by Grade'))      
print (mg)
       
### Reading Scores by Grade
# Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school
rgs = std.groupby(['grade','school_name'])['reading_score']
avg_rgs = pd.DataFrame(round(rgs.mean(),2))
rg = pd.concat([avg_rgs.loc['9th'], avg_rgs.loc['10th'], avg_rgs.loc['11th'], 
                avg_rgs.loc['12th']], axis=1, keys=['9th grade','10th grade',
                           '11th grade','12th grade'])
print ('Reading Scores by Grade')
print ('-'*len('Reading Scores by Grade'))       
print (rg)       
       
### Scores by School Spending
# Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending.
## Using Pandas cut, create a new column in the existing school_complete dataframe.
## Thid is the spending range bin which categorises the schools into Low, Medium, 
## High, or Prime based on their budget spending per student.
sch['sch_spending'] = pd.cut(sch['Per Student Budget'], 4, 
   labels=["Low","Medium","High", "Prime"])

##  Create a dataframe of schools based on their average spend  
sp = sch.groupby(['sch_spending','school_name'])['Average Math Score', 
                'Average Reading Score', '% Passing Math', '% Passing Reading', 
                'Overall Passing Rate']
ts = pd.DataFrame(sp.sum().dropna())
sr = pd.concat([ts.loc['Low'], ts.loc['Medium'], ts.loc['High'], 
                ts.loc['Prime']], keys=['Low', 'Medium', 'High', 'Prime'])                        
print ('Scores by School Spending')
print ('-'*len('Scores by School Spending'))       
print (ts)       

### Scores by School Size
# Repeat the above breakdown, but this time group schools based on a reasonable 
# approximation of school size (Small, Medium, Large).
sch['sch_size'] = pd.cut(sch['size'], 3, labels=["Small","Medium","Large"])

##  Create a dataframe of schools based on their student size  
tp = sch.groupby(['sch_size','school_name'])['Average Math Score', 
                'Average Reading Score', '% Passing Math', '% Passing Reading', 
                'Overall Passing Rate']
ss = pd.DataFrame(tp.sum().dropna())
print ('Scores by School Size')
print ('-'*len('Scores by School Size'))       
print (ss) 


### Scores by School Type
# Repeat the above breakdown, but this time group schools based on school type 
# (Charter vs. District).
##  Group the updated school_complete dataframe based on the school type
rt = sch.groupby(['type','school_name'])['Average Math Score', 
                 'Average Reading Score', '% Passing Math', '% Passing Reading', 
                 'Overall Passing Rate']
tt = pd.DataFrame(rt.sum().dropna())

print ('Scores by School Type')
print ('-'*len('Scores by School Type'))       
print (tt) 



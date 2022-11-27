#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
import streamlit as st


# @st.cache
def get_df(df):
    df.columns = [i.lower() for i in df.columns]
    df = df.rename(columns = {'creditscore':'credit_score','estimatedsalary':'estimated_salary'})
    age_25 = df['age'].quantile(0.25)
    age_5 = df['age'].quantile(0.5)
    age_75 = df['age'].quantile(0.75)
    credit_score_25 = df['age'].quantile(0.25)
    credit_score_5 = df['age'].quantile(0.5)
    credit_score_75 = df['age'].quantile(0.75)
    balance_25 = df['age'].quantile(0.25)
    balance_5 = df['age'].quantile(0.5)
    balance_75 = df['age'].quantile(0.75)
    estimated_salary_25 = df['age'].quantile(0.25)
    estimated_salary_5 = df['age'].quantile(0.5)
    estimated_salary_75 = df['age'].quantile(0.75)
    df.loc[(df['age']<age_25) ,'age_cluster' ] = 'age < ' + str(age_25)
    df.loc[(df['age']>=age_25) & (df['age']< age_5),'age_cluster' ] = str(age_25) + '<=' + 'age' + '<' + str(age_5)
    df.loc[(df['age']>=age_5) & (df['age']< age_75),'age_cluster' ] = str(age_5) + '<=' + 'age' + '<' + str(age_75)
    df.loc[(df['age']>=age_75) ,'age_cluster' ] = 'age > ' + str(age_75)
    df.loc[(df['credit_score']<credit_score_25) ,'credit_score_cluster' ] = 'credit_score < ' + str(credit_score_25)
    df.loc[(df['credit_score']>=credit_score_25) & (df['credit_score']< credit_score_5),'credit_score_cluster' ] = str(credit_score_25) + '<=' + 'credit_score' + '<' + str(credit_score_5)
    df.loc[(df['credit_score']>=credit_score_5) & (df['credit_score']< credit_score_75),'credit_score_cluster' ] = str(credit_score_5) + '<=' + 'credit_score' + '<' + str(credit_score_75)
    df.loc[(df['credit_score']>=credit_score_75) ,'credit_score_cluster' ] = 'credit_score > ' + str(credit_score_75)
    df.loc[(df['balance']<balance_25) ,'balance_cluster' ] = 'balance < ' + str(balance_25)
    df.loc[(df['balance']>=balance_25) & (df['credit_score']< balance_5),'balance_cluster' ] = str(balance_25) + '<=' + 'balance' + '<' + str(balance_5)
    df.loc[(df['balance']>=balance_5) & (df['credit_score']< balance_75),'balance_cluster' ] = str(balance_5) + '<=' + 'balance' + '<' + str(balance_75)
    df.loc[(df['balance']>=balance_75) ,'balance_cluster' ] = 'balance > ' + str(balance_75)
    df.loc[(df['estimated_salary']<estimated_salary_25) ,'estimated_salary_cluster' ] = 'estimated_salary < ' + str(estimated_salary_25)
    df.loc[(df['estimated_salary']>=estimated_salary_25) & (df['estimated_salary']< estimated_salary_5),'estimated_salary_cluster' ] = str(estimated_salary_25) + '<=' + 'estimated_salary' + '<' + str(estimated_salary_5)
    df.loc[(df['estimated_salary']>=estimated_salary_5) & (df['estimated_salary']< estimated_salary_75),'estimated_salary_cluster' ] = str(estimated_salary_5) + '<=' + 'estimated_salary' + '<' + str(estimated_salary_75)
    df.loc[(df['estimated_salary']>=estimated_salary_75) ,'estimated_salary_cluster' ] = 'estimated_salary > ' + str(estimated_salary_75)
    return df


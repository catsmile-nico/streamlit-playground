import numpy as np
import streamlit as st
import pandas as pd
from matplotlib.figure import Figure
import seaborn as sns

def barchart_pos_neg(df:pd.DataFrame):
    """ positive and negative bar chart

    Args:
        df (Dataframe): single col df with positive and negative values
    """
    col1, col2 = st.columns([1, 3])
    df["c"] = df["b"] = 0
    df = df.assign(b=np.where(df.a < 0, df.a, df.b), c=np.where(df.a > 0, df.a, df.c))
    df = df.iloc[:,1:3]
    with col1:
        st.dataframe(df)

    # dummy row0 to start from graph from 1
    dummydf = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns)
    df = pd.concat([dummydf, df], ignore_index=True)
    with col2:
        st.bar_chart(df)

def linechart_sns(df:pd.DataFrame):
    col1, col2 = st.columns([1, 3])

    df['index'] = range(1, len(df) + 1)
    df = df.assign(b=np.where(df.a < 0, "neg", "pos"))
    with col1:
        st.dataframe(df)
    df.reset_index(inplace=True)
    df = df[df['index'] != '']
    fig = Figure()
    ax = fig.subplots()
    sns.lineplot(x=df['index'], y=df['a'], hue=df['b'], ax=ax)
    ax.set_xlabel('index')
    ax.set_ylabel('a')
    with col2:
        st.pyplot(fig)

def main():
    barchart_pos_neg(pd.DataFrame(np.random.randn(25,1),columns=["a"]))
    linechart_sns(pd.DataFrame(np.random.randn(20, 2),columns=['a', 'b']))
    
if __name__ == '__main__':
    main()
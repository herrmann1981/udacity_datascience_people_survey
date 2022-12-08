import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_dataframe_histogram(df, columns=7):
    """
    This method can be used to plot the histogram of a dataset. That way we can style them all the same without
    repeating the code for it.
    :param df: The dataframe we want to plot the histogram for
    :param columns: The number of columns to plot the histogram
    :return: None
    """
    rows = int(df.shape[1] / columns) + 1
    df.hist(
        xlabelsize=6,  # Reduce x axis font size
        ylabelsize=6,  # Reduce y axis font size
        layout=(rows, columns),
        figsize=(20, rows*2)
    )
    plt.tight_layout()
    plt.show()


def plot_dataframe_correlation(df, corr_method='pearson'):
    """
    This method can be used to plot the correlation matrix of a dataframe as a heatmap
    :param df: The dataframe we want to plot
    :param corr_method: The pandas correlation method to be used.
    :return: None
    """
    df_corr = df.corr(method=corr_method, numeric_only=True)  
    fig, ax = plt.subplots(
        figsize=(35, 35)
    )
    ax.imshow(df_corr)

    # Show all ticks and label them with the dataframe column name
    ax.set_xticks(np.arange(df_corr.columns.shape[0]), labels=df_corr.columns)
    ax.set_yticks(np.arange(df_corr.columns.shape[0]), labels=df_corr.columns)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    plt.show()

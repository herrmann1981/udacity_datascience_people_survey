import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.linear_model
import sklearn.model_selection
import sklearn.metrics


def plot_dataframe_histogram(df: pd.DataFrame, columns=7):
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


def plot_dataframe_correlation(df: pd.DataFrame, corr_method='pearson'):
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


def plot_scores(x, train_scores, test_scores):
    """
    This function is used for plotting the score values for models for different test / train data splits
    :return: None
    """
    plt.plot(x, train_scores, label='Train Score', color='blue', linewidth=2)
    plt.plot(x, test_scores, label='Test Score', color='red', linewidth=2)
    plt.legend()
    plt.ylim(ymax=1.1, ymin=0)
    plt.show()

def preparation_correct_values(df: pd.DataFrame, columns, min=1, max=5):
    """
    This method is used for correcting values in certain columns to limit them to valid inputs.
    For this we are using our domain knowledge. For most of he questions only values between 1 and 5 are valid.
    Other values will be nulled.
    :param df: The dataframe where we want to correct the values
    :param columns: The list of columns where we want to check for min and max values
    :param min: This is the minimum allowed value in the columns
    :param max: This is the maximal allowed value in the columns
    :return: Corrected data frame. In the columns that are specified values that fall outside of the
        allowed range are set to null
    """
    df_result = df.copy()  # copy dataframe to avoid overwriting the original one
    for col in columns:
        df_result.loc[df_result[col] > max, col] = None
        df_result.loc[df_result[col] < min, col] = None

    return df_result


def preparation_clean_empty_cols(df: pd.DataFrame, threshold=1):
    """
    This method is used to remove columns where the amount of null values is above the given threshold
    :param df: The dataframe we want to clean
    :param threshold: The Threshold above we consider a column to be empty (1 = all rows empty, 0.5 = 50% empty rows)
    :return: The cleaned dataframe where empty columns have been removed
    """
    df_result = df.dropna(
        axis='columns',
        thresh=threshold
    )

    return df_result


def preparation_impute_values(df: pd.DataFrame):
    """
    This method is used to impute the mean value to numeric columns in rows where the value is none
    :param df: The dataframe where we want to impute values
    :return: Corrected dataframe
    """
    df_result = df.copy()  # copy dataframe to avoid overwriting the original
    try:
        for column in df_result.columns:  # iterate over all columns
            if df_result[column].dtype in ['int', 'float']:  # we only want to set the mean for int or float columns
                column_mean = df_result[column].mean()  # mean value for column
                df_result[column] = df_result[column].fillna(column_mean)  # actually filling null values with the mean
    except ValueError as error:
        print('Error during imputing values: %s' % str(error))
        raise error  # just raise the error again for now

    return df_result


def preparation_remove_categorical(df: pd.DataFrame):
    """
    This method is used to remove the categorical columns and replace them with dummy columns
    :param df: The dataframe where we want to replace the categorical values
    :return: The updated dataframe with no categorical columns, but with dummy columns instead
    """
    df_result = df.copy()
    for col in df.select_dtypes(include=['object']).columns:
        try:
            df_result = pd.concat(
                [
                    df_result,
                    pd.get_dummies(df_result[col],
                                   prefix=col,
                                   prefix_sep='_',
                                   drop_first=False,
                                   dummy_na=True)
                ],
                axis='columns')
            df_result = df_result.drop(col, axis='columns', inplace=False)
        except ValueError as error:
            print('Error during replacing categorical column with dummy columns: ' % str(error))
            continue  # Continue with the next column
    return df_result


def model_clean_fit(df: pd.DataFrame,
                    target_column: str,
                    test_size=0.25,
                    random_state=1,
                    model_selection='linearregression',
                    metric_method='r2'):
    """
    This method is responsible for fitting a flened dataset
    :param df: The cleaned dataframe we want to use for fitting our model
    :param target_column: The column name that we want to train
    :param test_size: Percentage value (0-1) that determines what percent of the data is used for training
    :param random_state: Controls the shuffling applied to the data before applying the test/train split
    :return x: The x column, meaning the values we want to predict
    :return y: The columns that are used to predict our x values
    :return x_train: The target column we want to predict (training set)
    :return y_train: The columns that are used to predict the target (training set)
    :return x_test: The target column we want to predict (test set)
    :return y_test: The test data to predict the x outputs (test set)
    :return train_score: The score of the model in regards to the training data.  Best possible score is 1.0
        (100 percent)
    :return test_score: The score of the model for the test data. Best possible score is 1.0
    """
    # Split the target column from the rest. The rest is used to predict the target
    x = df.drop(target_column, axis='columns')
    y = df[target_column]

    # Split our data into a training and a test set
    x_train, x_test, y_train, y_test = \
        sklearn.model_selection.train_test_split(x,
                                                 y,
                                                 test_size=test_size,
                                                 random_state=random_state )

    # Setup model and fit to the training data
    if model_selection == 'bayesianridge':
        model = sklearn.linear_model.BayesianRidge()
    else:
        model = sklearn.linear_model.LinearRegression()
    model.fit(x_train, y_train)

    #  now we want to predict how well our model behaves with the training data
    train_predict = model.predict(x_train)
    # and then we can predict the actual test data
    test_predict = model.predict(x_test)

    # Evaluate how well the model behaves
    if metric_method.lower() == 'percent':
        train_score = sklearn.metrics.mean_absolute_percentage_error(y_train, train_predict)
        test_score = sklearn.metrics.mean_absolute_percentage_error(y_test, test_predict)
    else:
        train_score = sklearn.metrics.r2_score(y_train, train_predict)
        test_score = sklearn.metrics.r2_score(y_test, test_predict)

    return x, y, x_train, y_train, x_test, y_test, train_score, test_score

import sqlite3
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LogNorm
import pandas as pd

# ========================= CLASS LABELS ========================= #

class_labels_all = ["deeplearning", "tensorflow", "scikit_learn", "bigdata", "aws",
                    "awscertifications", "css", "html", "javascript", "shittyprogramming",
                    "java", "sql", "learnsql", "postgresql", "softwarearchitecture", "scala",
                    "apachespark", "mongodb", "linux", "linux4noobs", "datascience", "machinelearning",
                    "etl", "python", "dataengineering"]


def get_random_class_labels(num=8):
    return np.random.choice(class_labels_all, num, replace=False)


# ========================= STOP WORDS ========================= #

useless_words = set(['postgres', 'big', 'panda', 'using', 'scikit', 'sklearn', 'apache', 'spark', 'lambda', 's3',
                     'does', 'looking', 'help', 'new', 'data', 'science', 'scientist', 'machine', 'learning', 'use',
                     'need', 'engineer', 'engineering'])

custom_stop_words = ENGLISH_STOP_WORDS.union(useless_words).union(set(class_labels_all))


def load_sqlite(database, query=None, class_labels=None):

    try:
        connection = sqlite3.connect(database)
    except Exception as e:
        print(f"The error '{e}' occurred connecting")

    placeholders = ','.join('?' for label in class_labels)

    ### FIX ###
    # this query needs to be explicitely given in each notebook
    # to allow for different databases
    subreddit_query = """
    SELECT
        title,
        subreddit,
        date
    FROM subreddits
    WHERE subreddit IN (%s);""" % str(placeholders)

    cursor = connection.cursor()
    cursor.execute(subreddit_query, class_labels)

    column_names = [description[0] for description in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data=data, columns=column_names)
    df = df.drop_duplicates(subset='title')
    for label in class_labels:
        if len(df[df['subreddit'] == label]) == 0:
            raise ValueError(f'No data for "{label}"')
    return df


def label_distribution(df, y, labels):
    '''Prints the number of rows per label'''
    for label in labels:
        print(f'{label}: {len(df[y == label])}')
    print()
    print(f'AVERAGE: {int(len(df) / len(labels))}')


def resample_to_average(df, y, labels):
    '''Resamples each label to the average number of posts across labels
    Note: Oversample AFTER splitting to train and test set in order to avoid duplicates between
        the train and test set which will give falsely better metrics
    '''
    average = int(len(df) / len(labels))
    resampled_df = pd.DataFrame()
    for label in labels:
        sampled_df = df[y == label].sample(n=average, replace=True)
        resampled_df = pd.concat([resampled_df, sampled_df])
    return resampled_df


def plot_confusion_matrix(model, y_true, y_pred, classes, cmap='Blues'):
    '''
    Plots confusion matrix for fitted model, better than scikit-learn version
    '''
    cm = confusion_matrix(y_true, y_pred)
    fontdict = {'fontsize': 16}
    fig, ax = plt.subplots(figsize=(2.2 * len(classes), 2.2 * len(classes)))

    sns.heatmap(cm,
                annot=True,
                annot_kws=fontdict,
                fmt="d",
                square=True,
                cbar=False,
                cmap=cmap,
                ax=ax,
                norm=LogNorm(),  # to get color diff on small values
                vmin=0.00001  # to avoid non-positive error for '0' cells
                )

    ax.set_xlabel('Predicted labels', fontdict=fontdict)
    ax.set_ylabel('True labels', fontdict=fontdict)
    ax.set_yticklabels(
        labels=classes, rotation='horizontal', fontdict=fontdict)
    ax.set_xticklabels(labels=classes, rotation=20, fontdict=fontdict)
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
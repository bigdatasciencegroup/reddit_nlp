"""
Preprocessors and estimators, along with their parameters for gridsearching.
Used with "compare_models" function from the Reddit class, Model class maybe
"""

import numpy as np
from sklearn.ensemble import (AdaBoostClassifier, BaggingClassifier,
                              ExtraTreesClassifier, GradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.feature_extraction.text import (ENGLISH_STOP_WORDS, TfidfVectorizer)
from sklearn.linear_model import (LogisticRegression,
                                  PassiveAggressiveClassifier, SGDClassifier)
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

# ========================= CLASS LABELS ========================= #

class_labels_all = ["deeplearning", "tensorflow", "scikit_learn", "pandas", "bigdata", "aws",
                    "awscertifications", "css", "html", "javascript", "shittyprogramming",
                    "java", "sql", "learnsql", "postgresql", "softwarearchitecture", "scala",
                    "apachespark", "mongodb", "linux", "linux4noobs", "datascience", "machinelearning",
                    "etl", "python", "dataengineering"]


def get_random_class_labels(num=8):
    return np.random.choice(class_labels_all, num, replace=False)


class_labels_random = get_random_class_labels()

# ========================= STOP WORDS ========================= #

useless_words = set(['postgres', 'big', 'panda', 'using', 'scikit', 'sklearn', 'apache', 'spark', 'lambda', 's3',
                     'does', 'looking', 'help', 'new', 'data', 'science', 'scientist', 'machine', 'learning', 'use',
                     'need', 'engineer', 'engineering'])

custom_stop_words = ENGLISH_STOP_WORDS.union(useless_words).union(set(class_labels_all))


# ========================= PREPROCESSORS ========================= #

preprocessors = {
    "tfidfvectorizer": {
        "name": "TfidVectorizer",
        "preprocessor": TfidfVectorizer(stop_words=custom_stop_words),
        "pipe_params": {
            # "tfidfvectorizer__strip_accents": [None, 'ascii', 'unicode'],
            "tfidfvectorizer__ngram_range": [(1, 2)],
            "tfidfvectorizer__max_features": [5000],
            "tfidfvectorizer__min_df": np.linspace(0, 1, 5),
            "tfidfvectorizer__max_df": np.linspace(0, 1, 5),
            "tfidfvectorizer__norm": ("l1", "l2"),
            "tfidfvectorizer__use_idf": [True, False]
        }
    }
}


# ========================= ESTIMATORS ========================= #

estimators = {
    'xgbclassifier': {
        'name': 'XGBoost Classifier',
        'estimator': XGBClassifier(),
        'pipe_params': {
            "xgbclassifier__hidden_layer_sizes": [10, 25, 50],
            "xgbclassifier__n_estimators": [50, 100, 200],
            "xgbclassifier__max_depth": [5, 10, 20]
        }
    },
    'mlpclassifier': {
        'name': 'Multi Layer Percetpron Classifier',
        'estimator': MLPClassifier(),
        'pipe_params': {
            "mlpclassifier__hidden_layer_sizes": [(100,), (250,), (500,)],
            "mlpclassifier__alpha": np.linspace(.0001, 1, 5),
            "mlpclassifier__activation": ['lbfgs', 'adam']
        }
    },
    "logisticregression": {
        "name": "Logistic Regression",
        "estimator": LogisticRegression(max_iter=1000),
        "pipe_params": {
            "logisticregression__penalty": ["l2"],
            "logisticregression__C": [.01, .1, 1, 3, 10],
            "logisticregression__solver": ["lbfgs", "saga"]
        }
    },
    "randomforestclassifier": {
        "name": "Random Forest",
        "estimator": RandomForestClassifier(),
        "pipe_params": {
            "randomforestclassifier__n_estimators": [100, 300],
            "randomforestclassifier__max_depth": np.linspace(5, 500, 5, dtype=int),
            "randomforestclassifier__min_samples_leaf": [1, 2, 3],
            "randomforestclassifier__min_samples_split": [.01, .05, .1]
        }
    },
    "kneighborsclassifier": {
        "name": "K Nearest Neighbors",
        "estimator": KNeighborsClassifier(),
        "pipe_params": {
            "kneighborsclassifier__n_neighbors": [3, 5, 7],
            "kneighborsclassifier__metric": ["manhattan"]
        }
    },
    "multinomialnb": {
        "name": "Multinomial Bayes Classifier",
        "estimator": MultinomialNB(),
        "pipe_params": {
            "multinomialnb__fit_prior": [False],
            "multinomialnb__alpha": [.01, .1, 1]
        }
    },
    "svc": {
        "name": "Support Vector Classifier",
        "estimator": SVC(),
        "pipe_params": {
            "svc__C": [1, 10, 100],
            "svc__kernel": ["rbf", "sigmoid", "poly"],
            "svc__gamma": ["scale"],
            "svc__probability": [False]
        }
    },
    "adaboostclassifier": {
        "name": "AdaBoost Classifier Logistic Regression",
        "estimator": AdaBoostClassifier(),
        "pipe_params": {
            "adaboostclassifier__learning_rate": [.001, .01, .1],
            "adaboostclassifier__n_estimators": [50, 100, 200],
            "adaboostclassifier__max_depth": [1, 2, 3]
        }
    },
    "baggingclassifierlog": {
        "name": "Bagging Classifier Logistic Regression",
        "estimator": BaggingClassifier(LogisticRegression(max_iter=1000)),
        "pipe_params": {
            "baggingclassifier__n_estimators": [50, 100, 200]
        }
    },
    "baggingclassifiermnb": {
        "name": "Bagging Classifier MultinomalNB",
        "estimator": BaggingClassifier(),
        "pipe_params": {
            "baggingclassifier__n_estimators": [50, 100, 200]
        }
    },
    "extratreesclassifier": {
        "name": "Extra Trees Classifier",
        "estimator": ExtraTreesClassifier(),
        "pipe_params": {
            "extratreesclassifier__bootstrap": [True, False],
            "extratreesclassifier__n_estimators": [100, 300, 500],
        }
    },
    "gradientboostingclassifier": {
        "name": "Gradient Boosting Classifier",
        "estimator": GradientBoostingClassifier(),
        "pipe_params": {
            "gradientboostingclassifier__max_depth": [None, 3, 5],
            "gradientboostingclassifier__n_estimators": [100, 300, 500]
        }
    },
    "passiveaggressiveclassifier": {
        "name": "Passive Agressive Classifier",
        "estimator": PassiveAggressiveClassifier(),
        "pipe_params":
            {
            "passiveaggressiveclassifier__C": np.linspace(0, 1, 5),
            "passiveaggressiveclassifier__fit_intercept": [True, False],
        }
    },
    "sgdclassifier": {
        "name": "Stochastic Gradient Descent Classifier",
        "estimator": SGDClassifier(),
        "pipe_params":
            {
            "sgdclassifier__alpha": np.linspace(.0001, .1, 5),
            "sgdclassifier__fit_intercept": [True, False],
            "sgdclassifier__l1_ratio": np.linspace(0, 1, 5),
            "sgdclassifier__penalty": ["l2", "l1", "elasticnet"],
        }
    },
    "nusvc": {
        "name": "NuSVC",
        "estimator": NuSVC(),
        "pipe_params":
            {
            "nusvc__nu": np.linspace(0, .9, 5),
            "nusvc__decision_function_shape": ["ovr", 'poly'],
            "nusvc__degree": [2, 3, 5]
        }
    },
    "linearsvc": {
        "name": "Linear SVC",
        "estimator": LinearSVC(),
        "pipe_params":
            {
            "linearsvc__C": np.linspace(0, 10, 5),
            "linearsvc__fit_intercept": [True, False],
        }
    }
}

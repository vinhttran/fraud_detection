import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, KFold, ShuffleSplit, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, r2_score, mean_squared_error, classification_report, make_scorer
from sklearn.metrics import average_precision_score
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

import tensorflow as tf
from tensorflow.keras.metrics import Precision, Recall
from tensorflow import keras


from pyspark.sql import SparkSession, Row
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

from surprise import Reader
from surprise import Dataset
from surprise import SVD
from surprise.model_selection import train_test_split


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,
                                                        random_state=4)

# SVM, Logistic Regression, Decision Trees, kNN
'''Logistic Regression'''
logistic = LogisticRegression(penalty=’l2’,
                            dual=False,
                            tol=0.0001,
                            C=1.0,
                            fit_intercept=True,
                            intercept_scaling=1,
                            class_weight=None,
                            random_state=None,
                            solver=’warn’,
                            max_iter=100,
                            multi_class=’warn’,
                            verbose=0,
                            warm_start=False, n_jobs=None, l1_ratio=None)
logistic.fit(X_train, y_train)
logistic_pred = logistic.predict(X_test)
print("precision:", average_precision_score(y_test, logistic_pred), "\n F1:", f1_score(y_test, logistic_pred))


'''Random Forest Decision Tree'''
rf = RandomForestClassifier(n_estimators=’warn’,
                            criterion=’gini’,
                            max_depth=None,
                            min_samples_split=2,
                            min_samples_leaf=1,
                            min_weight_fraction_leaf=0.0,
                            max_features=’auto’,
                            max_leaf_nodes=None,
                            min_impurity_decrease=0.0,
                            min_impurity_split=None,
                            bootstrap=True,
                            oob_score=False,
                            n_jobs=None,
                            random_state=None,
                            verbose=0,
                            warm_start=False,
                            class_weight=None)
rf.fit(X_train, y_train)
importances = rf.feature_importances_
RF_pred = rf.predict(X_test)
print("precision:", average_precision_score(y_test, RF_pred), "\n F1:", f1_score(y_test, RF_pred))


'''SVM'''
svm = svm.SVC(C=1.0,
            kernel=’rbf’,
            degree=3,
            gamma=’auto_deprecated’,
            coef0=0.0,
            shrinking=True,
            probability=False,
            tol=0.001,
            cache_size=200,
            class_weight=None,
            verbose=False,
            max_iter=-1,
            decision_function_shape=’ovr’,
            random_state=None)
svm.fit(X_train, y_train)
SVM_pred =  svm.predict(X_test)
print("precision:", average_precision_score(y_test, SVM_pred), "\n F1:", f1_score(y_test, SVM_pred))


'''KNN'''
knn = KNeighborsClassifier(n_neighbors=5,
                            weights=’uniform’,
                            algorithm=’auto’,
                            leaf_size=30,
                            p=2,
                            metric=’minkowski’,
                            metric_params=None,
                            n_jobs=None)
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)
#output precision score
knn_precision = average_precision_score(y_test, knn_pred)
print("precision:", average_precision_score(y_test, knn_pred), "\n F1:", f1_score(y_test, knn_pred))


'''Neural Net'''
model_activation = keras.models.Sequential()
n_hidden = 25
model_activation.add(keras.layers.Dense(units=n_hidden,
                                        input_dim=1,
                                        activation='sigmoid'))
model_activation.add(keras.layers.Dense(units=1))
model_activation.add(keras.layers.Dropout(rate=0.5))
model_activation.compile(loss='mean_squared_error',
                        optimizer='sgd',
                        metrics=['Precision'])
model_activation.fit(X_train, y_train,
                     epochs=10, batch_size=1, verbose = 0)


# RECOMMENDERS
'''Spark ALS Collaborative Filtering'''
spark = SparkSession.builder.getOrCreate()
als_model = ALS(
            itemCol='',
            userCol='',
            ratingCol='',
            nonnegative=True,
            maxIter=20,
            regParam=0.05,
            rank=20)
 #fit
sdf = spark.createDataFrame( #DF )
recommender = als_model.fit(sdf)
#predict
prediction = recommender.transform(sdf)#.toPandas().prediction
#evaluate
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                predictionCol="prediction")
als_rmse = evaluator.evaluate(predictions)
#https://jaceklaskowski.gitbooks.io/mastering-apache-spark/spark-mllib/spark-mllib-RegressionEvaluator.html


'''SVD'''
self.svd = SVD(n_factors= , n_epochs= , biased=True)
#https://surprise.readthedocs.io/en/stable/matrix_factorization.html#surprise.prediction_algorithms.matrix_factorization.SVD
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[["user","movie","rating"]], self.reader)
trainset = data.build_full_trainset()
self.svd.fit(trainset)
testdata = Dataset.load_from_df(requests[["user", "movie", "rating"]], self.reader)
#ask Ian for Tyler's code to loop through here
junk, testset = train_test_split(testdata, test_size=1)
SVD_pred = self.svd.test(testset)
#accuracy
svd_rmse = accuracy.rmse(SVD_pred)

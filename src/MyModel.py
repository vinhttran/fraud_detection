import numpy as np
import pickle

df=pd.read_json("data/data.json")
RF_data = pd.read_pickle('data/final_RF_data.pickle')


y = df["fraud"]
X = RF_data

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,
                                                        random_state=4)

rf = RandomForestClassifier(
                            n_estimators=100,
                            criterion='gini',
                            max_depth=50,
                            min_samples_split=3,
                            min_samples_leaf=1,
                            min_weight_fraction_leaf=0.0,
                            max_features='auto',
                            max_leaf_nodes=None,
                            min_impurity_decrease=0.0,
                            min_impurity_split=None,
                            bootstrap=True,
                            oob_score=False,
                            n_jobs=None,
                            random_state=None,
                            verbose=0,
                            warm_start=False,
                            class_weight=None
)
rf.fit(X_train, y_train)
importances = rf.feature_importances_
RF_pred = rf.predict(X_test)
print(classification_report(y_test, RF_pred))

pickle_out = open("models/RF_event_model_final.pkl","wb")
pickle.dump(rf, pickle_out)
pickle_out.close()

                                                    

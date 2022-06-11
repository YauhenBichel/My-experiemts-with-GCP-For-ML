@component(
    packages_to_install = [
        "pandas",
        "sklearn"
    ], base_image="python:3.9",
)
def winequality_evaluation(
    test_set:  Input[Dataset],
    rf_winequality_model: Input[Model],
    thresholds_dict_str: str,
    metrics: Output[ClassificationMetrics],
    kpi: Output[Metrics]
) -> NamedTuple("output", [("deploy", str)]):

    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd
    import logging 
    import pickle
    from sklearn.metrics import roc_curve, confusion_matrix, accuracy_score
    import json
    import typing

    
    def threshold_check(val1, val2):
        cond = "false"
        if val1 >= val2 :
            cond = "true"
        return cond

    data = pd.read_csv(test_set.path+".csv")
    model = RandomForestClassifier()
    file_name = rf_winequality_model.path + ".pkl"
    with open(file_name, 'rb') as file:  
        model = pickle.load(file)
    
    y_test = data.drop(columns=["target"])
    y_target=data.target
    y_pred = model.predict(y_test)
    

    y_scores =  model.predict_proba(data.drop(columns=["target"]))[:, 1]
    fpr, tpr, thresholds = roc_curve(
         y_true=data.target.to_numpy(), y_score=y_scores, pos_label=True
    )
    metrics.log_roc_curve(fpr.tolist(), tpr.tolist(), thresholds.tolist())  
    
    metrics.log_confusion_matrix(
       ["False", "True"],
       confusion_matrix(
           data.target, y_pred
       ).tolist(), 
    )
    
    accuracy = accuracy_score(data.target, y_pred.round())
    thresholds_dict = json.loads(thresholds_dict_str)
    rf_winequality_model.metadata["accuracy"] = float(accuracy)
    kpi.log_metric("accuracy", float(accuracy))
    deploy = threshold_check(float(accuracy), int(thresholds_dict['roc']))
    return (deploy,)
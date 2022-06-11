@component(
    packages_to_install = [
        "pandas",
        "sklearn",
    ], base_image="python:3.9",
)
def train_winequality(
    dataset:  Input[Dataset],
    model: Output[Model], 
):
    
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd
    import pickle

    data = pd.read_csv(dataset.path+".csv")
    model_rf = RandomForestClassifier(n_estimators=10)
    model_rf.fit(
        data.drop(columns=["target"]),
        data.target,
    )
    model.metadata["framework"] = "RF"
    file_name = model.path + f".pkl"
    with open(file_name, 'wb') as file:  
        pickle.dump(model_rf, file)

@dsl.pipeline(
    # Default pipeline root. You can override it when submitting the pipeline.
    pipeline_root=PIPELINE_ROOT,
    # A name for the pipeline. Use to determine the pipeline Context.
    name="pipeline-winequality",
    
)
def pipeline(
    url: str = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv",
    project: str = PROJECT_ID,
    region: str = REGION, 
    display_name: str = DISPLAY_NAME,
    api_endpoint: str = REGION+"-aiplatform.googleapis.com",
    thresholds_dict_str: str = '{"roc":0.8}',
    serving_container_image_uri: str = "europe-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest"
    ):
    
    data_op = get_wine_data(url)
    train_model_op = train_winequality(data_op.outputs["dataset_train"])
    model_evaluation_op = winequality_evaluation(
        test_set=data_op.outputs["dataset_test"],
        rf_winequality_model=train_model_op.outputs["model"],
        thresholds_dict_str = thresholds_dict_str, # I deploy the model anly if the model performance is above the threshold
    )
    
    with dsl.Condition(
        model_evaluation_op.outputs["deploy"]=="true",
        name="deploy-winequality",
    ):
           
        deploy_model_op = deploy_winequality(
        model=train_model_op.outputs['model'],
        project=project,
        region=region, 
        serving_container_image_uri = serving_container_image_uri,
        )
# Steps:
I. Set up up the environment
II. Install a virtual env and activate it inside the JupyterLab
III. Create the pipeline components: to load the data, train the model, evaluate the model, deploy the model.
IV. Create the pipeline
V. Run the pipeline
VI. Trigger the pipeline.

# I. Set up up the environment

If you like to activate the auto-completion in a notebook you should install the jupyter_contrib_nbextensions.
>!pip install jupyter_contrib_nbextensions
>!jupyter contrib nbextension install - user
>from jedi import settings
>settings.case_insensitive_completion = True

Install the kubeflow components.
- wine_uc_install_libs.py

Enable the APIs if they are not enabled.
- wine_uc_install_libs.py

Import the libraries.
- wine_uc_libs.py

Set up the global variables.
- global_env.py

# II. Install a virtual env and use it inside the JupyterLab



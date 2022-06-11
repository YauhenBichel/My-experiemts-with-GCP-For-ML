#Install virtual env 
python -m pip install --user virtualenv
echo "create env"
python -m venv vertex_venv
#Add kernel to jupyter
echo "Add kernel to jupyter"
ipython kernel install --name "vertex_env" --user
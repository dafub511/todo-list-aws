set -x
python3.7 -m venv todo-list-aws
source todo-list-aws/bin/activate
python3.7 -m pip install --upgrade pip
python3.7 -m pip install awscli
##python3.7 -m pip install aws-sam-cli
# For integration testing
python3.7 -m pip install pytest
python3.7 -m pip install requests
pwd

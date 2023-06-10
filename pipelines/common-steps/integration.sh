#!/bin/bash

source todo-list-aws/bin/activate
set -x
export BASE_URL=https://jjcb0j6rx6.execute-api.us-east-1.amazonaws.com/Prod
python3.7 -m pytest -s test/integration/todoApiTest.py

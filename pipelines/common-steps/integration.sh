#!/bin/bash

source todo-list-aws/bin/activate
set -x
export https://9o2chw1e2i.execute-api.us-east-1.amazonaws.com/Stage
python3.7 -m pytest -s test/integration/todoApiTest.py

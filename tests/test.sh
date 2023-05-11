#!/bin/bash
set -xe

TEST_ROOT=$(realpath $(dirname $0))
export PYTHONPATH=${PYTHONPATH}:${TEST_ROOT}

# install requirements
pip install -r ${TEST_ROOT}/requirements.txt

# backup orginal sample.py
cp ${TEST_ROOT}/sample.py ${TEST_ROOT}/.sample.py.bak

# clear testmon data
if [ -e ${TEST_ROOT}/../.testmondata ]; then
    rm ${TEST_ROOT}/../.testmondata
fi

# first run
pytest --testmon ${TEST_ROOT} | grep "collected 4 items"
# second run, all tests should be skipped
pytest --testmon ${TEST_ROOT} | grep "collected 0 items"

for i in 1 2 3 4; do
    # modify a method, one test should be run
    cp ${TEST_ROOT}/sample${i}.py ${TEST_ROOT}/sample.py
    pytest --testmon ${TEST_ROOT} | grep "collected 2 items / 1 deselected / 1 selected"
    # second run, all tests should be skipped
    pytest --testmon ${TEST_ROOT} | grep "collected 0 items"
done

# modify init, all tests should be run
cp ${TEST_ROOT}/sample5.py ${TEST_ROOT}/sample.py
pytest --testmon ${TEST_ROOT} | grep "collected 4 items"
# second run, all tests should be skipped
pytest --testmon ${TEST_ROOT} | grep "collected 0 items"

# restore sample.py
mv ${TEST_ROOT}/.sample.py.bak ${TEST_ROOT}/sample.py
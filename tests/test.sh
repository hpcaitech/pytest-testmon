#!/bin/bash
set -xe

TEST_ROOT=$(realpath $(dirname $0))

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


REPLACE_CMDS=(
    's/return self.rank/return self.rank + 1 - 1/'
    's/return self.world_size/return self.world_size + 1 - 1/'
    's/print("echo1")/print("call echo1")/'
    's/print("echo2")/print("call echo2")/'
)

for cmd in "${REPLACE_CMDS[@]}"; do
    # modify a method, one test should be run
    sed -i "${cmd}" ${TEST_ROOT}/sample.py
    pytest --testmon ${TEST_ROOT} | grep "collected 2 items / 1 deselected / 1 selected"
    # second run, all tests should be skipped
    pytest --testmon ${TEST_ROOT} | grep "collected 0 items"
done

# modify init, all tests should be run
sed -i 's/self.rank = rank/self.rank = rank + 1 - 1/' ${TEST_ROOT}/sample.py
pytest --testmon ${TEST_ROOT} | grep "collected 4 items"
# second run, all tests should be skipped
pytest --testmon ${TEST_ROOT} | grep "collected 0 items"

# restore sample.py
mv ${TEST_ROOT}/.sample.py.bak ${TEST_ROOT}/sample.py

# test coverage report
if [ -e ${TEST_ROOT}/../.coverage ]; then
    rm ${TEST_ROOT}/../.coverage
fi

coverage run --source ${TEST_ROOT} -m pytest ${TEST_ROOT}
coverage combine
coverage report -m > ${TEST_ROOT}/coverage.txt
rm ${TEST_ROOT}/../.coverage

rm ${TEST_ROOT}/../.testmondata
pytest --testmon --testmon-cov ${TEST_ROOT} ${TEST_ROOT}
coverage report -m > ${TEST_ROOT}/coverage_with_testmon.txt
rm ${TEST_ROOT}/../.coverage

diff ${TEST_ROOT}/coverage.txt ${TEST_ROOT}/coverage_with_testmon.txt
rm ${TEST_ROOT}/coverage.txt ${TEST_ROOT}/coverage_with_testmon.txt

export PYTHONPATH=${TEST_ROOT}/../
python ${TEST_ROOT}/check_pkg_change.py
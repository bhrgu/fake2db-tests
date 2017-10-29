# fake2db-tests
Several tests written with PyTest for the [fake2db](https://github.com/emirozer/fake2db) project.
Requirements: PyTest, Docker

#### An example of the test run for MySQL
Run test script with dockerized MySQL instance:
```
docker pull mysql:latest
mkvirtualenv -p python3 py3
workon py3
pip install -r ./requirements.txt
./run_mysql_tests.sh
```
or fill the existing test database with the fake2db and call the tests directly
(the example below shows the simple database filling and calling corresponding test suite):
```
fake2db --db mysql --host <HOST> --port <PORT> \
		--user <USER> --password <PASS> \
		--rows 1 --seed 1

ENV_HOST=<HOST> ENV_PORT=<PORT> \
ENV_USER=<USER> ENV_PASS=<PASS> \
py.test -v -s -m "SIMPLE_WITHOUT_NAME" test_mysql.py
```

#!/bin/bash

instance_name=mysql-fake2db-test
instance_host=127.0.0.1
port=3307
mysql_user=root
mysql_pass=s3cr3t

db_name_custom=CUSTOM_WITH_NAME
db_name_simple=SIMPLE_WITH_NAME

# Remove test container if it exists from previous runs
docker ps -a --no-trunc | grep $instance_name | awk '{print $1}' | xargs --no-run-if-empty docker rm

docker run --name $instance_name -e MYSQL_ROOT_PASSWORD=$mysql_pass -p $port:3306 -d mysql:latest

# Waiting for the mysql instance started
# cause it started twice, see https://github.com/docker-library/mysql/issues/245
echo "Waiting for DB connection..."
until $(docker logs $instance_name 2>&1 | egrep -q "mysqld.sock'  port: 3306")
do
    sleep 5
done

################ CUSTOM DB TESTS ##################

# Custom DB filling (unnamed)
fake2db --db mysql \
        --host $instance_host --port $port \
        --user $mysql_user --password $mysql_pass \
        --custom name date country \
        --rows 1 \
        --seed 1 # Seeding random generator if we need to check the data filled

# Run tests CUSTOM_WITHOUT_NAME
ENV_HOST=$instance_host ENV_PORT=$port \
ENV_USER=$mysql_user ENV_PASS=$mysql_pass \
py.test -v -s -m "CUSTOM_WITHOUT_NAME" test_mysql.py \
--html=mysql_custom_wo_name_test_log.html --self-contained-html

# Custom DB filling (named)
fake2db --db mysql \
        --host $instance_host --port $port \
        --user $mysql_user --password $mysql_pass \
        --custom name date country \
        --name $db_name_custom \
        --rows 1 \
        --seed 1 # Seeding random generator if we need to check the data filled

# Run tests CUSTOM_WITH_NAME
ENV_HOST=$instance_host ENV_PORT=$port \
ENV_USER=$mysql_user ENV_PASS=$mysql_pass \
ENV_DBNAME=$db_name_custom \
py.test -v -s -m $db_name_custom test_mysql.py \
--html=mysql_custom_with_name_test_log.html --self-contained-html

####################################################

################ SIMPLE DB TESTS ###################

# Simple DB filling (unnamed)
fake2db --db mysql \
        --host $instance_host --port $port \
        --user $mysql_user --password $mysql_pass \
        --rows 1 \
        --seed 1 # Seeding random generator if we need to check the data filled

# Run tests SIMPLE_WITHOUT_NAME
ENV_HOST=$instance_host ENV_PORT=$port \
ENV_USER=$mysql_user ENV_PASS=$mysql_pass \
py.test -v -s -m "SIMPLE_WITHOUT_NAME" test_mysql.py \
--html=mysql_simple_wo_name_test_log.html --self-contained-html

# Simple DB filling (named)
fake2db --db mysql \
        --host $instance_host --port $port \
        --user $mysql_user --password $mysql_pass \
        --name $db_name_simple \
        --rows 1 \
        --seed 1 # Seeding random generator if we need to check the data filled

# Run tests SIMPLE_WITH_NAME
ENV_HOST=$instance_host ENV_PORT=$port \
ENV_USER=$mysql_user ENV_PASS=$mysql_pass \
ENV_DBNAME=$db_name_simple \
py.test -v -s -m $db_name_simple test_mysql.py \
--html=mysql_simple_with_name_test_log.html --self-contained-html

####################################################

# Stopping dockerized MySQL instance
docker stop $instance_name

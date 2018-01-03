#!/bin/bash

db_name_custom=CUSTOM_WITH_NAME
db_name_simple=SIMPLE_WITH_NAME

################ CUSTOM DB TESTS ##################

# rm ./sqlite_*.db

# Custom DB filling (named)
fake2db --db sqlite \
        --custom name date country \
        --name $db_name_custom \
        --rows 1 \
        --seed 1 # Seeding random generator if we need to check the data filled

# Run tests CUSTOM_WITH_NAME
ENV_DBNAME=$db_name_custom \
py.test -v -s -l -m $db_name_custom test_sqlite.py \
--html=sqlite_custom_with_name_test_log.html --self-contained-html

rm ./$db_name_custom.db
####################################################

################ SIMPLE DB TESTS ###################

# Simple DB filling (named)
fake2db --db sqlite \
        --name $db_name_simple \
        --rows 1 \
        --seed 1 # Seeding random generator if we need to check the data filled

# Run tests SIMPLE_WITH_NAME
ENV_DBNAME=$db_name_simple \
py.test -v -s -m $db_name_simple test_sqlite.py \
--html=sqlite_simple_with_name_test_log.html --self-contained-html

rm ./$db_name_simple.db
####################################################

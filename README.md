# Udacity Data Pipeline Project
The purpose of this project was to build a data pipeline using Airflow that loads data from S3 to Amazon Redshift and executes some data quality checks.

## Airflow
This project is using airflow. Airflow is a platform to programmatically author, schedule and monitor workflows.
You can use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed.
Workflows are defined as code, and in hence become more maintainable, versionable, testable, and collaborative.

Source: [Airflow Documentation](https://airflow.apache.org/)

## Task

### Operators
Four operators were built that stage the data, transform the data, and run checks on data quality. All of the operators and task instances will run SQL statements against the Redshift database. 

#### Stage Operator
The stage operator loads any JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.

#### Fact & Dimension Operator
The dimension and fact operators execute statements from the SQL helper class to run data transformations. Most of the logic is within the SQL transformations and the operator is expected to take as input a SQL statement and target database on which to run the query against. You can also define a target table that will contain the results of the transformation. Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load.

#### Data Quality Operator
The Data Quality Operator is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. Result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.

## Data
The data was downloaded from Udacity's Resource page and uploaded onto a private AWS S3 bucket `s3://philsredshiftbucket`. This was necessary because my Redshift cluster was created in a different region than the official S3 Bucket from Udacity.

## Prerequisites
### Create tables
Before starting the workflow, all tables have to be created using the statements in `create_tables.sql`.

### Start you cluster
This pipeline uses a Postgres-Connection to Amazon Redshift. Create a cluster on AWS in order to know your endpoint/host for the next step.

### Add connections
In order to load data from S3 to Redshift you need to maintain Connections in the Airflow UI

1. Go to the Airflow UI:
2. Click on *Admin* tab and select *Connections*.
3. Click the *Create*-tab in the next screen.
4. On the create connection page, enter the following values:
- *Conn Id*: Enter aws_credentials.
- *Conn Type*: Enter Amazon Web Services.
- *Login*: Enter your Access key ID from the IAM User credentials you downloaded earlier.
- *Password*: Enter your Secret access key from the IAM User credentials you downloaded earlier.

Once you've entered these values, select *Save and Add Another*.

5. On the next create connection page, enter the following values:

- *Conn Id*: Enter redshift.
- *Conn Type*: Enter Postgres.
- *Host*: Enter the endpoint of your Redshift cluster, excluding the port at the end. You can find this by selecting your cluster in the Clusters page of the Amazon Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to NOT include the port at the end of the Redshift endpoint string.
Schema: Enter dev. This is the Redshift database you want to connect to.
- *Login*: Enter awsuser.
- *Password*: Enter the password you created when launching your Redshift cluster.
- *Port*: Enter 5439.

Once you've entered these values, select *Save*.

## How to start
Run /opt/airflow.start.sh to start the Airflow server. Access the Airflow UI by clicking Access Airflow button. Note that Airflow can take up to 10 minutes to create the connection due to the size of the files in S3.

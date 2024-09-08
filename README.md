# Project 3 Batch Processing Using Airflow and Spark

## Overview and Objective
From product need help to integrate data from our dwh to their product via API:
- Top Country Based on User
- Total Film Based on Category

## Tools
- Airflow on Local
- VSCode
- Dbeaver
- Docker
- PostgreSQL
- TiDB
- Dataset: https://www.kaggle.com/datasets/kapturovalexander/pagila-postgresql-sample-database

## Flow
![Flow](https://file.notion.so/f/f/01b24fa3-f906-4bbc-ae9a-eae8c32be7d8/32c7269a-4849-4425-bf0d-a7c1fb667885/image.png?table=block&id=0fc17910-9ab2-4e12-9d21-b0bd32002c60&spaceId=01b24fa3-f906-4bbc-ae9a-eae8c32be7d8&expirationTimestamp=1725904800000&signature=pkhBV9pU3nH51mTJhtsBuj4Cjn-a5UQSw_LuStWrvqs&downloadName=image.png)

## Step by Step
- Check connection DB server
    - Postgres
    - TiDB
- Run airflow on your local
    - Create file requirements.txt
    - Build images, Dockerfile
    - docker build -t my-airflow . 
    - Create docker compose, docker-compose.yaml
- Set connection on airflow
    - Postgres
    - TiDB
- Extract
    - Create module connector postgres
    - Create module get data from postgres
- Transform
    - Creae script for transformation data using spark
- Load
    - Create module connector for hadoop
    - create load data to hadoop
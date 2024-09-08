from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta, datetime


def fun_top_countries_get_data(**kwargs):
    spark = SparkSession.builder \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.0") \
        .master("local").appName("PySpark_Postgres").getOrCreate()
    
    df_country = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://34.42.78.12:5434/postgres") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "country") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .load()
    df_country.createOrReplaceTempView("country")
    
    df_city = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://34.42.78.12:5434/postgres") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "city") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .load()
    df_city.createOrReplaceTempView("city")
    
    df_result = spark.sql('''
        SELECT
            country,
            COUNT(country) as total,
            current_date() as date
        FROM country AS co
        INNER JOIN city AS ci
            ON ci.country_id = co.country_id
        GROUP BY country
    ''')
    
    df_result.write.mode('overwrite').partitionBy('date') \
        .option('compression', 'snappy') \
        .save('data_result-task_1')

def fun_top_countries_load_data(**kwargs):
    df = pd.read_parquet('data_result-task_1')
    engine = create_engine(
        'mysql+mysqlconnector://4FFFhK9fXu6JayE.root:9v07S0pKe4ZYCkjE@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test',
        echo=False)
    df.to_sql(name='top_country_suyanto', con=engine, if_exists='replace')

def fun_total_film_get_data(**kwargs):
    spark = SparkSession.builder \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.0") \
        .master("local").appName("PySpark_Postgres").getOrCreate()
    
    df_film = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://34.42.78.12:5434/postgres") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "film") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .load()
    df_film.createOrReplaceTempView("film")
    
    df_film_category = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://34.42.78.12:5434/postgres") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "film_category") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .load()
    df_film_category.createOrReplaceTempView("film_category")
    
    df_category = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://34.42.78.12:5434/postgres") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", "category") \
        .option("user", "airflow") \
        .option("password", "airflow") \
        .load()
    df_category.createOrReplaceTempView("category")
    
    df_result = spark.sql('''
        SELECT
            name,
            COUNT(name) as total,
            current_date() as date
        FROM (
                SELECT *
                FROM film AS f
                JOIN film_category as fc
                ON f.film_id = fc.film_id) AS j
        JOIN category AS c
            ON j.category_id = c.category_id
        GROUP BY name
        ORDER BY COUNT(name) DESC
    ''')
    
    df_result.write.mode('overwrite').partitionBy('date') \
        .option('compression', 'snappy') \
        .save('data_result-task_2')

def fun_total_film_load_data(**kwargs):
    df = pd.read_parquet('data_result-task_2')
    engine = create_engine(
        'mysql+mysqlconnector://4FFFhK9fXu6JayE.root:9v07S0pKe4ZYCkjE@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test',
        echo=False)
    df.to_sql(name='total_film_suyanto', con=engine, if_exists='replace')


with DAG(
    dag_id='d_1_batch_processing_spark',
    start_date=datetime(2022, 5, 28),
    schedule_interval='00 23 * * *',
    catchup=False
) as dag:

    start_task = EmptyOperator(
        task_id='start'
    )

    op_top_countries_get_data = PythonOperator(
        task_id='top_countries_get_data',
        python_callable=fun_top_countries_get_data,
        execution_timeout=timedelta(minutes=6)
    )
        
    op_top_countries_load_data = PythonOperator(
        task_id='top_countries_load_data',
        python_callable=fun_top_countries_load_data,
        execution_timeout=timedelta(minutes=6)
    )

    op_total_film_get_data = PythonOperator(
        task_id='total_film_get_data',
        python_callable=fun_total_film_get_data,
        execution_timeout=timedelta(minutes=6)
    )
        
    op_total_film_load_data = PythonOperator(
        task_id='total_film_load_data',
        python_callable=fun_total_film_load_data,
        execution_timeout=timedelta(minutes=6)
    )
    
    end_task = EmptyOperator(
        task_id='end'
    )
    
    start_task >> op_top_countries_get_data >> op_top_countries_load_data >> end_task
    start_task >> op_total_film_get_data >> op_total_film_load_data >> end_task
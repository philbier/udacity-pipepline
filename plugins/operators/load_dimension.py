from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    
    sql_truncate = "TRUNCATE TABLE {}"

    sql_insert = "INSERT INTO {} {}"

    @apply_defaults
    def __init__(self,
                 table='',
                 redshift_conn_id='',
                 sql='',
                 append_data=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        self.append_data = append_data
        
    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.append_data == True:
            redshift.run(LoadDimensionOperator.sql_insert)
        else:
            redshift.run(LoadDimensionOperator.sql_truncate.format(self.table))
            redshift.run(LoadDimensionOperator.sql_insert.format(self.table, self.sql))

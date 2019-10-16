from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 table='',
                 redshift_conn_id='',
                 sql='',
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        
    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
   
        redshift.run("DELETE FROM public.{}".format(self.table))
        
        redshift.run("TRUNCATE TABLE {}; INSERT INTO {} {}".format(self.table, self.table, self.sql))

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 table='',
                 check_sql='',
                 expected_result='',
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.check_sql = check_sql
        self.expected_result = expected_result
        
        
    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        table = self.table
        sql = self.check_sql
        expected_result = self.expected_result
        
        records = redshift.get_records(sql.format(table))[0][0]
        if records != expected_result:
            self.log.info("Test '{}' has failed".format(sql))
            self.log.info("{} != {} records".format(records, expected_result))
        else:
            self.log.info("Test '{}' has succeeded".format(sql))
            self.log.info("{} == {} records".format(records, expected_result))
          

        
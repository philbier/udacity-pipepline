from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'
    
    check_sql = """
    SELECT count(*)
    FROM {}
    """
    
    check_column_sql = """
    SELECT count(*)
    FROM {}
    WHERE {} is NULL
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 tables=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables
        
    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        for table in self.tables:
            self.log.info("General Check: Check NULL-Values in {} tables".format(table))
            count = redshift.get_records("SELECT count(*) FROM {}".format(table))
            if len(count) == 0 or len(count[0]) == 0:
                raise ValueError("Check failed - no records found")
            self.log.info("Check for {} successful".format(table))

        self.log.info("Specific Check: check table songid in songplays table")
        formattedSql = DataQualityOperator.check_column_sql.format(
            "songplays",
            "songid"
        )
        count_userId = redshift.get_records(formattedSql)
        if len(count_userId) == 0:
            self.log.info("Data quality check for songid in songplays : Successful - No errors found")
        else:
            self.log.info("Data quality check for songid in songplays : Failed - {}".format(count_userId[0]))
        
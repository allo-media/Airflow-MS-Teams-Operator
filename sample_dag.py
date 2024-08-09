import pendulum

from airflow.decorators import dag, task

from ms_teams_powerautomate_webhook_operator import MSTeamsPowerAutomateWebhookOperator

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def sample_dag():

    @task()
    def get_formatted_date(**kwargs):
        iso8601date = kwargs['execution_date'].strftime("%Y-%m-%dT%H:%M:%SZ")
        formatted_date = f"{{{{DATE({iso8601date}, SHORT)}}}} at {{{{TIME({iso8601date})}}}}"
        print(formatted_date)
        return formatted_date
        
    formatted_date = get_formatted_date()

    op1 = MSTeamsPowerAutomateWebhookOperator(task_id='send_to_teams',
        http_conn_id='msteams_webhook_url',
        heading_message="Airflow local test",
        heading_subtitle=formatted_date,
        body_message="**lorem_ipsum** ran successfully in **localhost**",
        button_text="View logs",
        button_url="http://localhost:8080",
        )



sample_dag()

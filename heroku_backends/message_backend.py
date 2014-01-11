from kombu import Connection
import os
_broker_url = os.environ.get("RABBITMQ_BIGWIG_URL")
if _broker_url:
    connection = Connection(_broker_url)
else:
    connection = Connection(transport="memory")

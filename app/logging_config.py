from loguru import logger
import httpx
# Loki configuration
# loki_config = {
#     "sink": "loki",
#     "https://reddivari.grafana.net/api/v1/push",
#     # "url": "http://loki:3100/loki/api/v1/push",
#     "serialize": False
# }

# Configure Loguru logger
# removing default logger
logger.remove()
# logger.add(**loki_config)

logger.add(
    "https://684816:glc_eyJvIjoiOTM2NTU5IiwibiI6InN0YWNrLTczMTc4My1obC1ncmFmYW5hbG9raS1zbWFydC1pbXMiLCJrIjoiMTE0VXAyWTdoN2pUOTB2WFFENXNrMEhYIiwibSI6eyJyIjoicHJvZC1hcC1zb3V0aGVhc3QtMSJ9fQ==@logs-prod-020.grafana.net/loki/api/v1/push",
    serialize=True,  # Serialize logs as JSON
    level="INFO",  # Adjust the log level as needed
    backtrace=True,  # Include Python tracebacks in logs
)
print("Within logger config")


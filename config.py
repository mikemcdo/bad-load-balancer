import os
import logging
from enum import Enum


_MAX_NODE_CONNECTIONS = 500
UPDATE_INTERVAL = int(os.environ.get("UPDATE_INTERVAL", 60))
MIN_NUMBER_OF_SERVERS = int(os.environ.get("MIN_NUMBER_OF_SERVERS", 2))
_MAX_ACCEPTABLE_LOAD_FOR_ENVIRONMENT = float(
    os.environ.get("MAX_ACCEPTABLE_LOAD", 0.75)
)
_LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
MAX_LOAD = _MAX_ACCEPTABLE_LOAD_FOR_ENVIRONMENT * _MAX_NODE_CONNECTIONS
API_BASE_URL = "http://bad_load_balancer:8188"
HEADERS = {"Accept": "application/json, application/problem+json"}


class LoadBalancerRoutes(Enum):
    GET_NODE = "/loadbalancer/node/{node}"
    GET_NODE_LIST = "/loadbalancer/node_list"
    GET_STATS = "/loadbalancer/stats"

    POST_DISABLE_NODE = "/loadbalancer/node/{node}/disable"
    POST_ENABLE_NODE = "/loadbalancer/node/{node}/enable"

    DELETE_STATS = "/loadbalancer/stats"


logging.basicConfig(level=getattr(logging, _LOG_LEVEL, logging.INFO))

logging.info("System started...")
logging.info(f"UPDATE_INTERVAL: {UPDATE_INTERVAL}")
logging.info(f"MIN_NUMBER_OF_SERVERS: {MIN_NUMBER_OF_SERVERS}")
logging.info(
    f"MAX_ACCEPTABLE_LOAD_FOR_ENVIRONMENT: {_MAX_ACCEPTABLE_LOAD_FOR_ENVIRONMENT}"
)
logging.info(f"MAX_LOAD: {MAX_LOAD}")
logging.info(f"LOG_LEVEL: {_LOG_LEVEL}")
logging.info(f"API_BASE_URL: {API_BASE_URL}")

import requests

import config


def get_formatted_api_url(route, node=None):
    return f"{config.API_BASE_URL}{route.value}".format(node=node)


def make_get_request(route, node=None):
    url = get_formatted_api_url(route, node)
    try:
        response = requests.get(url, headers=config.HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        config.logging.error(
            f"GET request to route {route} node {node} has failed with: {err}"
        )
        raise err


def make_post_request(route, node):
    url = get_formatted_api_url(route, node)
    try:
        response = requests.post(url, headers=config.HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        config.logging.error(
            f"POST request to route {route} node {node} has failed with: {err}"
        )
        raise err


def make_delete_request(route):
    url = get_formatted_api_url(route)
    try:
        response = requests.delete(url, headers=config.HEADERS)
        response.raise_for_status()
        return response
    except Exception as err:
        config.logging.error(f"DELETE request to route {route} has failed with: {err}")
        raise err


def get_node_list():
    return make_get_request(config.LoadBalancerRoutes.GET_NODE_LIST)["nodes"]


def get_node(node):
    return make_get_request(config.LoadBalancerRoutes.GET_NODE, node)


def get_stats():
    return make_get_request(config.LoadBalancerRoutes.GET_STATS)


def disable_node(node):
    return make_post_request(config.LoadBalancerRoutes.POST_DISABLE_NODE, node)


def enable_node(node):
    return make_post_request(config.LoadBalancerRoutes.POST_ENABLE_NODE, node)


def delete_stats():
    return make_delete_request(config.LoadBalancerRoutes.DELETE_STATS)


# Helper function for testing
def enable_all_nodes():
    for node in get_node_list():
        enable_node(node)

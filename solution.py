#!/usr/bin/env python3
import time

import config
import api_service


def get_nodes_and_status():
    nodes = []
    for node_name in api_service.get_node_list():
        node = api_service.get_node(node_name)
        nodes.append(node)
    return nodes


def disable_nodes_over_capacity(maximum_disabled_nodes):
    nodes = get_nodes_and_status()
    total_nodes_disabled = 0

    for node in nodes:
        if node_should_be_disabled(maximum_disabled_nodes, node, total_nodes_disabled):
            config.logging.info(
                f"Disabling node {node['node']}, queued requests: {node['queued_requests']}"
            )
            api_service.disable_node(node["node"])
            total_nodes_disabled += 1
        elif not node["enabled"]:
            total_nodes_disabled += 1
    return total_nodes_disabled


def node_should_be_disabled(maximum_disabled_nodes, node, total_nodes_disabled):
    return (
        node["enabled"]
        and node["queued_requests"] > config.MAX_LOAD
        and total_nodes_disabled < maximum_disabled_nodes
    )


def enable_nodes_under_capacity():
    nodes = get_nodes_and_status()
    for node in nodes:
        if node_should_be_enabled(node):
            config.logging.info(
                f"Enabling node {node['node']}, queued requests: {node['queued_requests']}"
            )
            api_service.enable_node(node["node"])


def node_should_be_enabled(node):
    return not node["enabled"] and node["queued_requests"] < config.MAX_LOAD


def manage_load_balancer():
    while True:
        config.logging.info("Checking server status...")
        nodes = get_nodes_and_status()
        enable_nodes_under_capacity()
        maximum_disabled_nodes = len(nodes) - config.MIN_NUMBER_OF_SERVERS
        disable_nodes_over_capacity(maximum_disabled_nodes)
        config.logging.info("Waiting for next update...")
        time.sleep(config.UPDATE_INTERVAL)


if __name__ == "__main__":
    manage_load_balancer()

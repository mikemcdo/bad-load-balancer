import pytest
from unittest import mock

import config
import solution


def test_get_current_system_status():
    expected_number_of_nodes = 20
    nodes = solution.get_nodes_and_status()
    assert len(nodes) == expected_number_of_nodes


@mock.patch("config.MAX_LOAD", 100)
def test_node_should_be_disabled_when_eligible():
    # too many requests, and less than max disabled
    node = {"enabled": True, "queued_requests": 150}
    assert solution.node_should_be_disabled(5, node, 3)


@mock.patch("config.MAX_LOAD", 100)
def test_node_should_be_disabled_when_not_eligible():
    # node is already disabled
    node = {"enabled": False, "queued_requests": 150}
    assert not solution.node_should_be_disabled(5, node, 3)

    # node doesn't exceed max connections
    node = {"enabled": True, "queued_requests": 50}
    assert not solution.node_should_be_disabled(5, node, 3)

    # already enough nodes disabled
    node = {"enabled": True, "queued_requests": 150}
    assert not solution.node_should_be_disabled(5, node, 5)


@mock.patch("config.MAX_LOAD", 100)
def test_node_should_be_enabled_when_eligible():
    # Case 1: Node should be enabled (disabled, and below MAX_LOAD)
    node = {"enabled": False, "queued_requests": 50}
    assert solution.node_should_be_enabled(node)


@mock.patch("config.MAX_LOAD", 100)
def test_node_should_be_enabled_when_not_eligible():

    # Case 2: Node should NOT be enabled (disabled, but exceeds MAX_LOAD)
    node = {"enabled": False, "queued_requests": 150}
    assert not solution.node_should_be_enabled(node)

    # Case 3: Node should NOT be enabled (already enabled)
    node = {"enabled": True, "queued_requests": 50}
    assert not solution.node_should_be_enabled(node)

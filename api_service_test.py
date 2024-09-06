import pytest

import config
import api_service


@pytest.fixture
def setup_teardown():
    # Reset the API before the test
    api_service.enable_all_nodes()
    yield
    # Reset the API after the test
    api_service.enable_all_nodes()


def assert_response_contains_expected_fields(response, expected_fields):
    for field in expected_fields:
        assert field in response


@pytest.mark.unit
def test_get_formatted_api_url_with_no_params():
    assert (
        api_service.get_formatted_api_url(config.LoadBalancerRoutes.GET_NODE_LIST)
        == "http://bad_load_balancer:8188/loadbalancer/node_list"
    )


@pytest.mark.unit
def test_get_formatted_api_url_with_params():
    test_node = "node1"
    assert (
        api_service.get_formatted_api_url(config.LoadBalancerRoutes.GET_NODE, test_node)
        == f"http://bad_load_balancer:8188/loadbalancer/node/{test_node}"
    )


@pytest.mark.integration
def test_get_stats(setup_teardown):
    expected_fields = ["$schema", "load_balancer_stats"]
    response = api_service.get_stats()
    assert_response_contains_expected_fields(response, expected_fields)


@pytest.mark.integration
def test_get_node_list(setup_teardown):
    expected_number_of_nodes = 20
    response = api_service.get_node_list()
    assert len(response) == expected_number_of_nodes


@pytest.mark.integration
def test_get_node(setup_teardown):
    node_name = "server-01"
    expected_fields = ["$schema", "node", "enabled", "queued_requests"]
    response = api_service.get_node(node_name)
    assert_response_contains_expected_fields(response, expected_fields)


@pytest.mark.integration
def test_enable_and_disable_node(setup_teardown):
    node_name = "server-01"
    # Ensure the node is enabled
    assert api_service.get_node(node_name)["enabled"] is True

    # Disable the node
    response = api_service.disable_node(node_name)
    assert response["enabled"] is False

    # Enable the node
    response = api_service.enable_node(node_name)
    assert response["enabled"] is True

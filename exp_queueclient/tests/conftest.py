import pytest

from exp_queueclient import BlueskyHttpserverSession


@pytest.fixture
def bluesky_httpserver_url():
    return "http://localhost:60610"


@pytest.fixture
def bluesky_httpserver_session(bluesky_httpserver_url):
    """
    A factory-as-a-fixture.
    """

    def bluesky_httpserver_session_():
        return BlueskyHttpserverSession(bluesky_httpserver_url=bluesky_httpserver_url)

    return bluesky_httpserver_session_

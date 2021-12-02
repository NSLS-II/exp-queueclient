import time as ttime

from contextlib import contextmanager

import pytest

from exp_queueclient import BlueskyHttpserverSession


@pytest.fixture
def bluesky_httpserver_url():
    return "http://localhost:60610"


@pytest.fixture
def clean_bluesky_httpserver_session(bluesky_httpserver_url):
    """
    A factory-as-a-fixture-and-context-manager.
    """

    @contextmanager
    def _clean_bluesky_httpserver_session(bluesky_httpserver_url_=None):
        if bluesky_httpserver_url_ is None:
            bluesky_httpserver_url_ = bluesky_httpserver_url

        try:
            session = BlueskyHttpserverSession(
                bluesky_httpserver_url=bluesky_httpserver_url_
            )
            session.environment_destroy()
            session.history_clear()
            session.queue_clear()
            ttime.sleep(3)

            yield None

        finally:
            session.history_clear()
            session.queue_clear()
            session.environment_destroy()
            ttime.sleep(3)

    return _clean_bluesky_httpserver_session

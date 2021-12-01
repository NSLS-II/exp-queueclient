import time as ttime

from exp_queueclient import BlueskyHttpserverSession


def test_environment_context_manager(bluesky_httpserver_url):
    """
    This test is successful if no exception is raised.
    """
    session = BlueskyHttpserverSession(bluesky_httpserver_url=bluesky_httpserver_url)
    session.environment_close()
    ttime.sleep(5)
    status_response = session.status()
    assert status_response.json()["worker_environment_exists"] is False

    with BlueskyHttpserverSession(
        bluesky_httpserver_url=bluesky_httpserver_url
    ) as bluesky_httpserver_session:
        # it seems to be important to wait a bit before closing the environment
        ttime.sleep(5)
        status_response = bluesky_httpserver_session.status()
        assert status_response.json()["worker_environment_exists"] is True

    # this pause following 'environment close' seems to be important as well
    ttime.sleep(5)

    status_response = session.status()
    assert status_response.json()["worker_environment_exists"] is False


def test_status(bluesky_httpserver_url):
    session = BlueskyHttpserverSession(bluesky_httpserver_url=bluesky_httpserver_url)
    status_response = session.status()
    assert status_response.json()["worker_environment_exists"] is False


# this test can cause trouble with other tests - infinite looping in one case
# def test_queue_mode_set(bluesky_httpserver_url):
#     session = BlueskyHttpserverSession(bluesky_httpserver_url=bluesky_httpserver_url)
#     queue_mode_set_response = session.queue_mode_set(queue_mode_key="loop", queue_mode_value=True)
#     assert queue_mode_set_response.status_code == 200
#     queue_mode_set_response = session.queue_mode_set(queue_mode_key="loop", queue_mode_value=False)
#     assert queue_mode_set_response.status_code == 200


def test_plan(bluesky_httpserver_url):
    with BlueskyHttpserverSession(
        bluesky_httpserver_url=bluesky_httpserver_url
    ) as bluesky_httpserver_session:
        ttime.sleep(2)
        bluesky_httpserver_session.queue_item_add(
            item_name="count", item_args=[["det1", "det2"]], item_type="plan"
        )
        ttime.sleep(2)
        bluesky_httpserver_session.queue_start()
        ttime.sleep(5)

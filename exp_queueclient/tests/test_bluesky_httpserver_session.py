import time as ttime

from exp_queueclient import BlueskyHttpserverSession


def test_environment_context_manager(bluesky_httpserver_url):
    """
    This test is successful if no exception is raised.
    """
    session = BlueskyHttpserverSession(bluesky_httpserver_url=bluesky_httpserver_url)
    status_response = session.status()
    if status_response.json()["worker_environment_exists"]:
        session.environment_close()
        ttime.sleep(5)
    status_response = session.status()
    assert status_response.json()["worker_environment_exists"] is False

    with BlueskyHttpserverSession(
        bluesky_httpserver_url=bluesky_httpserver_url
    ) as bluesky_httpserver_session:

        # it seems to be important to wait a bit before closing the environment
        status_response = bluesky_httpserver_session.status()
        while status_response.json()["worker_environment_exists"] is False:
            ttime.sleep(1)
            status_response = bluesky_httpserver_session.status()
        assert status_response.json()["worker_environment_exists"] is True

    # this pause following 'environment close' seems to be important as well
    status_response = bluesky_httpserver_session.status()
    while status_response.json()["worker_environment_exists"] is True:
        ttime.sleep(1)
        status_response = bluesky_httpserver_session.status()

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


def test_plan(clean_bluesky_httpserver_session, bluesky_httpserver_url):
    with clean_bluesky_httpserver_session():
        with BlueskyHttpserverSession(
            bluesky_httpserver_url
        ) as bluesky_httpserver_session_:
            # important to wait for environment to open
            #   is there a better way?
            #   session.wait_for_status("worker_environment_exists", True) ?
            ttime.sleep(3)

            status_response = bluesky_httpserver_session_.status()
            assert status_response.json()["items_in_queue"] == 0
            assert status_response.json()["running_item_uid"] is None

            queue_item_add_response = bluesky_httpserver_session_.queue_item_add(
                item_name="count",
                item_args=[["det1", "det2"]],
                item_kwargs={"num": 3, "delay": 1},
                item_type="plan",
            )
            print(queue_item_add_response.json())
            assert queue_item_add_response.json()["success"] is True

            status_response = bluesky_httpserver_session_.status()
            assert status_response.json()["items_in_queue"] == 1

            queue_start_response = bluesky_httpserver_session_.queue_start()
            print(f"queue_start_response:\n{queue_start_response.json()}")
            assert queue_start_response.json()["success"] is True

            # wait for the queue to start
            bluesky_httpserver_session_.wait_for_status(
                target_status={"running_item_uid": 0}
            )

            status_response = bluesky_httpserver_session_.status()
            running_item_uid = status_response.json()["running_item_uid"]
            assert running_item_uid is not None

            bluesky_httpserver_session_.wait_for_status(
                target_status={"running_item_uid": None}
            )

            # check the history for our plan

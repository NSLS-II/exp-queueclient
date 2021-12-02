import logging
import time as ttime

import requests


from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


class BlueskyHttpserverSession:
    def __init__(self, bluesky_httpserver_url):
        """
        Parameters
        ----------
        bluesky_httpserver_url: str
          URI specifying host and port, eg. "http://localhost:60610"
        """
        log = logging.getLogger(self.__class__.__name__)

        self._bluesky_httpserver_url = bluesky_httpserver_url
        log.debug("self.bluesky_httpserver_url: '%s'", self._bluesky_httpserver_url)

    def __enter__(self):
        # TODO: store the response in case someone wants to see it
        environment_open_response = self.environment_open()
        if environment_open_response.json()["success"] is False:
            raise Exception(
                f"failed to open an environment\n{environment_open_response.json()}"
            )
        return self

    def __exit__(self, *exc):
        # TODO: store the response in case someone wants to see it
        self.environment_close()
        # not so useful to check for failure since that means there is was open environment
        return False

    def httpserver_get(self, endpoint, **kwargs):
        log = logging.getLogger(self.__class__.__name__)

        endpoint_url = f"{self._bluesky_httpserver_url}/{endpoint}"
        log.debug("GET url: '%s', kwargs: '%s'", endpoint_url, dict(kwargs))
        endpoint_response = requests.get(url=endpoint_url, **kwargs)
        log.debug(
            "GET response: '%s', elapsed time: '%s's, ",
            endpoint_response,
            endpoint_response.elapsed,
        )
        return endpoint_response

    def httpserver_post(self, endpoint, **kwargs):
        log = logging.getLogger(self.__class__.__name__)

        endpoint_url = f"{self._bluesky_httpserver_url}/{endpoint}"
        log.debug("POST url: '%s', kwargs: '%s'", endpoint_url, dict(kwargs))
        endpoint_response = requests.post(url=endpoint_url, **kwargs)
        log.debug(
            "POST response: '%s', elapsed time: '%s's, ",
            endpoint_response,
            endpoint_response.elapsed,
        )
        return endpoint_response

    def wait_for_status(self, target_status, max_status_checks=3):
        """Wait for self.status() to match the specified target_status.

        Parameters
        ----------
        target_status:
            subset of status response JSON:
                (qserver) vagrant@vagrant:~$ qserver status
                Arguments: ['status']
                20:05:16 - MESSAGE:
                {'devices_allowed_uid': 'a2f32d48-22dd-487a-ac9e-852964adbc4f',
                 'items_in_history': 0,
                 'items_in_queue': 1,
                 'manager_state': 'idle',
                 'msg': 'RE Manager',
                 'pause_pending': False,
                 'plan_history_uid': '0269bc0e-e024-4367-b28b-df796f5e1d94',
                 'plan_queue_mode': {'loop': False},
                 'plan_queue_uid': '6a23166e-d5b1-403b-a985-88577e89f222',
                 'plans_allowed_uid': '66b3a3e0-916f-41fd-9b2d-0ac76d1e7748',
                 'queue_stop_pending': False,
                 're_state': 'idle',
                 'run_list_uid': '1d70095c-853a-4a3d-84ed-8b3cbb215824',
                 'running_item_uid': None,
                 'worker_environment_exists': True}
        max_status_checks:
            positive integer number of status checks with 1s sleep between checks

        Returns
        -------
            True if the target status has been achieved, False otherwise
        """
        for _ in range(max_status_checks):
            status_response = self.status()
            status_json = status_response.json()

            if all(
                [
                    status_json[target_status_key] == target_status_value
                    for target_status_key, target_status_value in target_status.items()
                ]
            ):
                return True
            else:
                print(f"status:\n{status_json}")
                print(f"does not match target status:\n{target_status}")
                ttime.sleep(1)

        return False

    def environment_open(self):
        """Open a qserver environment.

        Client code should prefer the context manager protocol to calling this method directly, for example:

            with BlueskyHttpserverSession(bluesky_httpserver_url="http://localhost:60610") as session:
                ...

        """

        return self.httpserver_post(endpoint="environment/open")

    def environment_close(self):
        """Close the HTTP session.

        This is the counterpart to `environment_open`. Client code should prefer the context manager protocol.

        """
        return self.httpserver_post(endpoint="environment/close")

    def environment_destroy(self):
        return self.httpserver_post(endpoint="environment/destroy")

    def status(self):
        return self.httpserver_get("status")

    def queue_mode_set(self, queue_mode_key, queue_mode_value):
        queue_mode_json = {"mode": {queue_mode_key: queue_mode_value}}
        return self.httpserver_post("queue/mode/set", json=queue_mode_json)

    def queue_get(self):
        return self.httpserver_get("queue/get")

    def queue_clear(self):
        return self.httpserver_post("queue/clear")

    def queue_start(self):
        return self.httpserver_post("queue/start")

    def queue_stop(self):
        return self.httpserver_post("queue/stop")

    def queue_stop_cancel(self):
        return self.httpserver_post("queue/stop/cancel")

    def queue_item_add(
        self, item_name, item_args=None, item_kwargs=None, item_type="plan"
    ):
        if item_args is None:
            item_args = []

        if item_kwargs is None:
            item_kwargs = {}

        item_json = {
            "item": {
                "name": item_name,
                "args": item_args,
                "kwargs": item_kwargs,
                "item_type": item_type,
            }
        }
        return self.httpserver_post("queue/item/add", json=item_json)

    def queue_item_execute(self, item_name, item_args, item_type):
        item_json = {
            "item": {"name": item_name, "args": item_args, "item_type": item_type}
        }
        return self.httpserver_post("queue/item/execute", json=item_json)

    def queue_item_add_batch(self):
        raise NotImplementedError()

    def queue_upload_spreadsheet(self):
        raise NotImplementedError()

    def queue_item_update(self):
        raise NotImplementedError()

    def queue_item_remove(self):
        raise NotImplementedError()

    def queue_item_remove_batch(self):
        raise NotImplementedError()

    def queue_item_move(self):
        raise NotImplementedError()

    def queue_item_move_batch(self):
        raise NotImplementedError()

    def queue_item_get(self):
        raise NotImplementedError()

    def history_get(self):
        return self.httpserver_get("history/get")

    def history_clear(self):
        return self.httpserver_post("history/clear")

    def re_pause(self):
        raise NotImplementedError()

    def re_resume(self):
        raise NotImplementedError()

    def re_stop(self):
        raise NotImplementedError()

    def re_abort(self):
        return self.httpserver_post(endpoint="re/abort")

    def re_halt(self):
        raise NotImplementedError()

    def re_runs_active(self):
        raise NotImplementedError()

    def re_runs_open(self):
        raise NotImplementedError()

    def re_runs_closed(self):
        raise NotImplementedError()

    def plans_allowec(self):
        raise NotImplementedError()

    def devices_allowed(self):
        raise NotImplementedError()

    def permissions_reload(self):
        raise NotImplementedError()

    def manager_stop(self):
        raise NotImplementedError()

    def test_manager_kill(self):
        # probably don't really need this
        raise NotImplementedError()

    def stream_console_output(self):
        # probably don't really need this
        raise NotImplementedError()

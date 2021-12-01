import logging

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
        self.environment_open()
        # useful to put a pause here?
        return self

    def __exit__(self, *exc):
        self.environment_close()
        # useful to put a pause here?
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

    def environment_open(self):
        """Open a qserver environment.

        Client code should prefer the context manager protocol to calling this method directly, for example:

            with BlueskyHttpserverSession(bluesky_httpserver_url="http://localhost:60610") as session:
                ...

        """

        self.httpserver_post(endpoint="environment/open")

    def environment_close(self):
        """Close the HTTP session.

        This is the counterpart to `environment_open`. Client code should prefer the context manager protocol.

        """
        self.httpserver_post(endpoint="environment/close")

    def environment_destroy(self):
        self.httpserver_post(endpoint="environment/destroy")

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

    def queue_item_add(self, item_name, item_args, item_type):
        item_json = {
            "item": {"name": item_name, "args": item_args, "item_type": item_type}
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
        raise NotImplementedError()

    def history_clear(self):
        raise NotImplementedError()

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

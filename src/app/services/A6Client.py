# -*- coding: utf-8 -*-

import logging
from urllib.parse import urljoin

import requests

_logger = logging.getLogger(__name__)


class A6Client(object):
    def __init__(self, host, api_key=None):
        if not host:
            raise Exception("no host arg specified")

        self.base_uri = urljoin(host, "/apisix/admin/")
        self.timeout = 30
        self.api_key = api_key

        self.headers = {}
        if self.api_key:
            self.headers["X-API-KEY"] = self.api_key

    def do_api(self, method, path, body=None):
        """Effectue une requête API vers APISIX."""
        try:
            r = requests.request(
                method,
                urljoin(self.base_uri, path),
                json=body,
                headers=self.headers,
                timeout=self.timeout,
            )
            response = r.json()

            if r.status_code >= 300:
                error_msg = response.get("error_msg", "") or response.get(
                    "message", "Unknown error"
                )
                _logger.warning(f"{method} {path} failed: {r.status_code} - {error_msg}")
                return None

            return response
        except requests.RequestException as e:
            _logger.error(f"Erreur de requête pour {method} {path}: {e}")
            return None

    def new_route(self, **kwargs):
        if not kwargs.get("uris"):
            raise Exception("no uris specified")

        http_verb = "POST"
        url = "routes/"
        route_id = kwargs.get("route_id", None)
        if route_id:
            http_verb = "PUT"
            url += str(route_id)

        response = self.do_api(http_verb, url, kwargs)
        route_id = response["key"].split("/")[-1] if response else None
        return int(route_id) if route_id else None

    def get_route(self, route_id):
        if not route_id:
            raise Exception("no route_id specified")

        return self.do_api("GET", f"routes/{route_id}")

    def update_route(self, **kwargs):
        route_id = kwargs.get("route_id")
        if not route_id:
            raise Exception("no route_id specified")

        response = self.do_api("PUT", f"routes/{route_id}", kwargs)
        return int(response["key"].split("/")[-1]) if response else None

    def del_route(self, route_id):
        if not route_id:
            raise Exception("no route_id specified")

        return self.do_api("DELETE", f"routes/{route_id}")

    def new_upstream(self, **kwargs):
        if not kwargs.get("type") or not kwargs.get("nodes"):
            raise Exception("Type and nodes are required for upstream")

        http_verb = "POST"
        url = "upstreams/"
        upstream_id = kwargs.get("upstream_id", None)
        if upstream_id:
            http_verb = "PUT"
            url += str(upstream_id)

        response = self.do_api(http_verb, url, kwargs)
        upstream_id = response["key"].split("/")[-1] if response else None
        return int(upstream_id) if upstream_id else None

    def get_upstream(self, upstream_id):
        if not upstream_id:
            raise Exception("no upstream_id specified")

        return self.do_api("GET", f"upstreams/{upstream_id}")

    def update_upstream(self, **kwargs):
        upstream_id = kwargs.get("upstream_id")
        if not upstream_id:
            raise Exception("no upstream_id specified")

        response = self.do_api("PUT", f"upstreams/{upstream_id}", kwargs)
        return int(response["key"].split("/")[-1]) if response else None

    def del_upstream(self, upstream_id):
        if not upstream_id:
            raise Exception("no upstream_id specified")

        return self.do_api("DELETE", f"upstreams/{upstream_id}")

    def new_service(self, **kwargs):
        if not kwargs.get("type") or not kwargs.get("nodes"):
            raise Exception("Type and nodes are required for upstream")

        http_verb = "POST"
        url = "services/"
        service_id = kwargs.get("service_id", None)
        if service_id:
            http_verb = "PUT"
            url += str(service_id)

        response = self.do_api(http_verb, url, kwargs)
        service_id = response["key"].split("/")[-1] if response else None
        return int(service_id) if service_id else None

    def new_consumer(self, **kwargs):
        if not kwargs.get("username"):
            raise Exception("Username is required for consumer")

        username = kwargs["username"]
        http_verb = "PUT"
        url = f"consumers/{username}"

        response = self.do_api(http_verb, url, kwargs)
        return response if response else None

    def del_consumer(self, username):
        if not username:
            raise Exception("no username specified")
        return self.do_api("DELETE", f"consumers/{username}")

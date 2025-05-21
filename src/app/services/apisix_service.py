# -*- coding: utf-8 -*-

import logging
import os

from .A6Client import A6Client

_logger = logging.getLogger(__name__)


class ApiSixService:
    def __init__(self):
        self.admin_url = os.getenv("APISIX_ADMIN_URL")
        self.api_key = os.getenv("APISIX_API_KEY")

        if not self.admin_url or not isinstance(self.admin_url, str):
            raise ValueError("APISIX URL is missing or invalid.")

        if not self.api_key or not isinstance(self.api_key, str):
            raise ValueError("APISIX API key is missing or invalid.")

        try:
            self.client = A6Client(self.admin_url, self.api_key)
            _logger.info("APISIX client initialized successfully.")
        except Exception as e:
            _logger.error(f"Error initializing APISIX client: {e}")
            raise

    def create_service(self, service_name, upstream_nodes):
        """Create an APISIX service."""
        service_data = {
            "name": service_name,
            "upstream": {"type": "roundrobin", "nodes": upstream_nodes},
        }

        try:
            response = self.client.new_service(service_data)
            _logger.info(f"Service '{service_name}' successfully created: {response}")
            return response
        except Exception as e:
            _logger.error(f"Error creating service '{service_name}': {e}")
            return None

    def create_route(self, route_id, uri, upstream_id, methods=None, plugins=None):
        """Create an APISIX route."""
        if methods is None:
            methods = ["GET", "POST"]
        if plugins is None:
            plugins = {}

        route_data = {
            "uri": uri,
            "methods": methods,
            "upstream_id": upstream_id,
            "plugins": plugins,
        }

        try:
            response = self.client.new_route(route_data)
            _logger.info(f"Route '{route_id}' successfully created: {response}")
            return response
        except Exception as e:
            _logger.error(f"Error creating route '{route_id}': {e}")
            return None

    def create_consumer(self, username, api_key, labels=None, limit_count=None):
        """Creates an APISIX consumer with optional labels and limit-count plugin."""
        plugins = {
            "key-auth": {"key": api_key},
        }

        if limit_count:
            plugins["limit-count"] = {
                "count": limit_count.get("count", 1),
                "time_window": limit_count.get("time_window", 10),
                "rejected_code": limit_count.get("rejected_code", 429),
                "key": limit_count.get("key", "consumer_name"),
                "policy": limit_count.get("policy", "local"),
            }

        consumer_data = {
            "username": username,
            "plugins": plugins,
        }

        if labels:
            consumer_data["labels"] = labels

        try:
            response = self.client.new_consumer(**consumer_data)
            _logger.info(f"Consumer '{username}' created successfully: {response}")
            return response
        except Exception as e:
            _logger.error(f"Error creating consumer '{username}': {e}")
            return None

    def delete_consumer(self, username):
        """Delete an APISIX consumer by username."""
        if not username:
            _logger.error("Username is required to delete consumer")
            return None

        try:
            response = self.client.del_consumer(username)
            if response and response.get("deleted") == "1":
                _logger.info(f"Consumer '{username}' deleted successfully.")
            else:
                _logger.warning(
                    f"Consumer '{username}' could not be deleted or does not exist: {response}"
                )
            return response
        except Exception as e:
            _logger.error(f"Error deleting consumer '{username}': {e}")
            return None

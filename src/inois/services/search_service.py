from inois.application_properties import *
from inois.utils.notifications import Notifications
import requests
import logging
import json


class SearchService:

    @classmethod
    def search_on_all_queries(cls, search_queries, session):
        logging.info(Notifications.EXECUTING_SEARCH)
        print("\n" + Notifications.EXECUTING_SEARCH)

        for query in search_queries:
            cls.execute_query(query, search_queries[query], session)

    @staticmethod
    def execute_query(search_datum, possible_hash_list, session):
        logging.info(Notifications.CURRENT_DATUM_QUERY.format(search_datum))
        print(Notifications.CURRENT_DATUM_QUERY.format(search_datum))

        api_response = requests.post(
            INOIS_API_URL + INOIS_API_SEARCH_URL,
            headers={'Authorization': 'Bearer ' + session['access_token']},
            json={'query': possible_hash_list}
        )

        if not api_response:
            logging.error(Notifications.DATUM_QUERY_FAILED.format(search_datum, api_response.status_code))
            raise RuntimeError(Notifications.DATUM_QUERY_FAILED.format(search_datum, api_response.status_code))

        response_json = json.loads(api_response.text)
        logging.info(Notifications.DATUM_QUERY_SUCCESSFUL.format(len(response_json)))
        print(Notifications.DATUM_QUERY_SUCCESSFUL.format(len(response_json)))
        print(json.dumps(response_json, indent=2))



from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .stix_transmission.ping_connector import PingConnector
from .stix_transmission.delete_connector import DeleteConnector
from .stix_transmission.results_connector import ResultsConnector
from .stix_transmission.api_client import APIClient
from .stix_translation.query_translator import QueryTranslator
from .stix_translation.results_translator import ResultsTranslator
import os

class EntryPoint(BaseEntryPoint):

    # python main.py translate virus_total results '{}' "[ipv4-addr:value = '127.0.0.1']"

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        if connection:
            api_client = APIClient(connection, configuration)
            base_sync_connector = BaseSyncConnector()
            ping_connector = PingConnector(api_client)
            query_connector = base_sync_connector
            status_connector = base_sync_connector
            results_connector = ResultsConnector(api_client)
            delete_connector = DeleteConnector(api_client)

            self.set_results_connector(results_connector)
            self.set_status_connector(status_connector)
            self.set_delete_connector(delete_connector)
            self.set_query_connector(query_connector)
            self.set_ping_connector(ping_connector)

        # Use default translation setup with default dialect otherwise...
        # self.setup_translation_simple(dialect_default='default')

        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, "stix_translation"))

        dialect = 'default'
        query_translator = QueryTranslator(options, dialect, filepath)
        results_translator = ResultsTranslator(options, dialect, filepath)
        self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator, default=True)
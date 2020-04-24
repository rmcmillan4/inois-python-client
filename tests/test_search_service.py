import pytest
from inois.services.search_service import SearchService


class TestSearchServiceClass:

    def test_search_on_all_queries_without_authorization(self):
        with pytest.raises(RuntimeError):
            mock_query = {'123456789': 'fjdiaosjfiaofp898a8fads='}
            mock_sessipn = {'access_token': '6798697698'}
            SearchService.search_on_all_queries(mock_query, mock_sessipn)

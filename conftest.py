import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import pytest

pytest_plugins = ['docker_compose']


@pytest.fixture(scope='session', autouse=True)
def wait_for_api(session_scoped_container_getter):
    """Wait for the services ready. Ideally we should have wait for
    all services, however here we only wait for the HTTP inteface of
    Elasticsearch because it usually the last service to be ready, and
    its HTTP interface is easy to wait for.
    """
    print('Waiting for ElasticSearch to be ready...')
    request_session = requests.Session()
    retries = Retry(total=20,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    service = session_scoped_container_getter.get('elasticsearch').network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert request_session.get(api_url)
    return request_session, api_url

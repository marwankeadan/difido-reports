import pytest

@pytest.fixture
def host(request):
    return request.config.getini('host')

def test_hello_world(host):
    assert host == '192.168.10.1'
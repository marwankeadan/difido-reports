# -*- coding: utf-8 -*-


def test_bar_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_sth(difido_conf):
            assert difido_conf.host == "192.168.1.1"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--host=192.168.1.1',
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'difido:',
        '*--host=DEST_HOST*Difido server host address.',
    ])


def test_hello_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        host = 192.168.10.1
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def host(request):
            return request.config.getini('host')

        def test_hello_world(host):
            assert host == '192.168.10.1'
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

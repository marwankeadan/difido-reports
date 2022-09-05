# -*- coding: utf-8 -*-

import pytest

from time import localtime, strftime

from difido import config, ReportElementStatus, ReportElementType
from difido.reporter import Reporter

difido_suite_name = None  # type: str
difido_test_name = None  # type: str
testAttr = {}
reporter = Reporter()


def pytest_addoption(parser):
    group = parser.getgroup('difido')
    group.addoption(
        '--host',
        action='store',
        dest='dest_host',
        default=config.host,
        help='Difido server host address.'
    )
    group.addoption(
        '--port',
        action='store',
        dest='dest_port',
        default=config.port,
        help='Difido server port address.'
    )
    group.addoption(
        '--exe_description',
        action='store',
        dest='dest_execution_description',
        default=config.execution_description,
        help='Difido execution description.'
    )
    parser.addini('host', 'Difido server host address.')
    parser.addini('port', 'Difido server port address.')
    parser.addini('exe_description', 'Difido execution description.')


@pytest.fixture(autouse=True)
def difido_conf(request):
    config.host = request.config.option.dest_host
    config.port = request.config.option.dest_port
    config.execution_description = request.config.option.dest_execution_description
    return config

@pytest.fixture(scope="session")
def report():
    return Reporter()


def pytest_runtest_setup(item):
    global testAttr
    # testAttr = {'starttime': strftime("%Y%m%d %H:%M:%S", localtime()), 'doc': "",
    #             'className': item.nodeid.split("::")[1].replace("Test", "")}
    testAttr = {'starttime': strftime("%Y%m%d %H:%M:%S", localtime()), 'doc': "",
                'className': item.nodeid}

    reporter.start_test(item.name, testAttr)


def pytest_runtest_logreport(report):
    if report.when == 'call':
        if report.outcome == 'failed':
            testAttr['status'] = ReportElementStatus.ERROR
            reporter.report("", "<pre>" + str(report.longreprtext) + "</pre>", element_type=ReportElementType.HTML,
                            status=ReportElementStatus.ERROR)
        else:
            testAttr['status'] = ReportElementStatus.SUCCESS

        reporter.end_test(difido_test_name, testAttr)


def pytest_sessionfinish(session):
    reporter.end_suite(difido_suite_name, testAttr)
    reporter.close()


def pytest_collection_finish(session):
    """ called after collection has been performed and modified.
    :param _pytest.main.Session session: the pytest session object
    """
    reporter.start_suite(config.execution_description, testAttr)

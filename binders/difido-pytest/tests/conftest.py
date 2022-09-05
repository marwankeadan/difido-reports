import pytest

from infra.reporter import Reporter
from infra.test_details import ReportElementStatus, ReportElementType
from time import localtime, strftime
import time
from infra.configuration import Conf

difido_suite_name = None  # type: str
difido_test_name = None  # type: str
testAttr = {}
reporter = Reporter()


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

    conf = Conf("remote")
    description = conf.get_string("description")
    reporter.start_suite(description, testAttr)

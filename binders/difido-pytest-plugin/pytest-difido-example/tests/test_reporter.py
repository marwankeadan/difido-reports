from difido import ReportElementStatus


def test_pass(report):
    report.log("Log message")
    report.add_execution_properties("int_Execution", "66")
    report.add_test_property("double_testProp", "1.56")


def test_fail(report):
    report.log("Log message", ReportElementStatus.FAILURE)


def test_warning(report):
    report.log("Log message", ReportElementStatus.WARNING)


def test_error(report):
    report.log("Log message", ReportElementStatus.ERROR)


def test_exception(report):
    raise Exception("Purposed Exception")


def test_assertion(report):
    assert 1 == 0


def test_levels(report):
    report.start_level("Level")
    report.log("Level Test")
    report.stop_level()

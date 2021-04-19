# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Wrapper for ``llnl.util.retry``"""

import pytest
import llnl.util.retry

try:
    import urllib.request as urllib
except ImportError:
    import urllib2 as urllib  # type: ignore  # novm


# keep track of how many retries done
count = 0


class MockFailureResponse(object):

    def __init__(self):
        global count
        count += 1
        raise Exception("This is a mocked failure.")


def test_retry(monkeypatch):
    """Test that retry works as expected
    """
    global count

    def mock_fail(*args, **kwargs):
        return MockFailureResponse()

    # apply the monkeypatch for urlopen to mock_fail
    monkeypatch.setattr(urllib, "urlopen", mock_fail)
    request = urllib.Request("https://google.com")

    # This first request must fail
    with pytest.raises(Exception):
        urllib.urlopen(request)

    # Now do function with retry
    @llnl.util.retry.retry
    def mock_fail(*args, **kwargs):
        return MockFailureResponse()

    count = 0
    monkeypatch.setattr(urllib, "urlopen", mock_fail)
    with pytest.raises(Exception):
        urllib.urlopen(request)

    assert count == 5

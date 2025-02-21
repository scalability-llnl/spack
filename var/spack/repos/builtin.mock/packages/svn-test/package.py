# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SvnTest(Package):
    """Mock package that uses svn for fetching."""

    url = "http://www.example.com/svn-test-1.0.tar.gz"

    version("svn", svn="to-be-filled-in-by-test")

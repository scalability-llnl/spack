# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CvsTest(Package):
    """Mock package that uses cvs for fetching."""

    homepage = "http://www.cvs-fetch-example.com"

    version("cvs", cvs="to-be-filled-in-by-test")

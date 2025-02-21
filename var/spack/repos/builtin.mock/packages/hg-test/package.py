# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HgTest(Package):
    """Test package that does fetching with mercurial."""

    homepage = "http://www.hg-fetch-example.com"

    version("hg", hg="to-be-filled-in-by-test")

# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class UrlTest(Package):
    """Mock package that fetches from a URL."""
    homepage = "http://www.url-fetch-example.com"

    version('test', url='to-be-filled-in-by-test')

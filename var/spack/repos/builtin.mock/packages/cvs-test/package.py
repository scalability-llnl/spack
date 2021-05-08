# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CvsTest(Package):
    """Mock package that uses cvs for fetching."""
    homepage = "http://www.cvs-fetch-example.com"

    version('cvs', cvs='to-be-filled-in-by-test')

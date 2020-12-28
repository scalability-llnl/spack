# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFastmatch(RPackage):
    """Package providing a fast match() replacement for cases that require
       repeated look-ups. It is slightly faster that R's built-in match()
       function on first match against a table, but extremely fast on any
       subsequent lookup as it keeps the hash table in memory."""

    homepage = "http://www.rforge.net/fastmatch"
    url      = "https://cloud.r-project.org/src/contrib/fastmatch_1.1-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fastmatch"

    version('1.1-0', sha256='20b51aa4838dbe829e11e951444a9c77257dcaf85130807508f6d7e76797007d')

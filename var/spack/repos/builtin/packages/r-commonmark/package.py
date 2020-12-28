# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCommonmark(RPackage):
    """commonmark: CommonMark and Github Markdown Rendering in R"""

    homepage = "https://cloud.r-project.org/package=commonmark"
    url      = "https://cloud.r-project.org/src/contrib/commonmark_1.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/commonmark/"

    version('1.7', sha256='d14a767a3ea9778d6165f44f980dd257423ca6043926e3cd8f664f7171f89108')

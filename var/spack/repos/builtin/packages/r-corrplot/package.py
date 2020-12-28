# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCorrplot(RPackage):
    """A graphical display of a correlation matrix or general matrix.
    It also contains some algorithms to do matrix reordering."""

    homepage = "https://cloud.r-project.org/package=corrplot"
    url      = "https://cloud.r-project.org/src/contrib/corrplot_0.77.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/corrplot"

    version('0.84', sha256='0dce5e628ead9045580a191f60c58fd7c75b4bbfaaa3307678fc9ed550c303cc')
    version('0.77', sha256='54b66ff995eaf2eee3f3002509c6f27bb5bd970b0abde41893ed9387e93828d3')

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNortest(RPackage):
    """nortest: Tests for Normality

       Five omnibus tests for testing the composite hypothesis of normality."""

    homepage = "https://cloud.r-project.org/package=nortest"
    url      = "https://cloud.r-project.org/src/contrib/nortest_1.0-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nortest"

    version('1.0-4', sha256='a3850a048181d5d059c1e74903437569873b430c915b709808237d71fee5209f')

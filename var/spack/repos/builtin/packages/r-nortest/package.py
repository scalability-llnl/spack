# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNortest(RPackage):
    """Tests for Normality.

    Five omnibus tests for testing the composite hypothesis of normality."""

    cran = "nortest"

    license("GPL-2.0-or-later")

    version("1.0-4", sha256="a3850a048181d5d059c1e74903437569873b430c915b709808237d71fee5209f")

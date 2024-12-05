# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RZlibbioc(RPackage):
    """An R packaged zlib-1.2.5.

    This package uses the source code of zlib-1.2.5 to create libraries for
    systems that do not have these available via other means (most Linux and
    Mac users should have system-level access to zlib, and no direct need
    for this package). See the vignette for instructions on use."""

    bioc = "zlibbioc"

    version("1.46.0", commit="f475457ece2c2b5fc9e6a91a3084dcba2345ab0a")
    version("1.44.0", commit="d39f0b02fa108ab907b4042c00a114569430a333")
    version("1.42.0", commit="aa074d72515df745ad65133ca21d3cad778ccc0e")
    version("1.40.0", commit="3f116b39d104c1ea8288f6b8f0ef94bb95f41f69")
    version("1.36.0", commit="62e888cd7fb482d512c6c31961b657e0b924e357")
    version("1.30.0", commit="99eae5b05968bf6abc9b54b9031afd93517381e0")
    version("1.28.0", commit="b825b042742ba45455fc284b988ff4cd2a33222c")
    version("1.26.0", commit="2e3ab097caa09a5e3ddaa3469b13e19a7224da0d")
    version("1.24.0", commit="2990059338d1b987d098c009b0bfa806bd24afec")
    version("1.22.0", commit="30377f830af2bc1ff17bbf3fdd2cb6442015fea5")

    depends_on("c", type="build")  # generated

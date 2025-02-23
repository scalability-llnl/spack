# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
#     spack install xalt
#
# You can edit this file again by typing:
#
#     spack edit xalt
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Xalt(AutotoolsPackage):
    """XALT is a lightweight software tool for any Linux cluster, workstation,
    or high-end supercomputer to track executable information and linkage of static
    shared and dynamically linked libraries. When the code is executed, wrappers intercept
    both GNU linker (ld) to capture linkage information and environmental variables."""

    homepage = "https://xalt.readthedocs.io/en/latest/index.html"
    url = "https://github.com/xalt/xalt/archive/refs/tags/xalt-2.10.45.tar.gz"

    # notify when the package is updated.
    maintainers("jflics6460")

    version("2.10.45", sha256="c10898402111b230eac1c0d3769a4b46361c97fc3415977c2199b5db3de8c547")

    depends_on("lmod")
    depends_on("lua")

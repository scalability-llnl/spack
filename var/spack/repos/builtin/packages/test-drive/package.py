# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TestDrive(MesonPackage):
    """Simple testing framework for Fortran packages"""

    homepage = "https://github.com/fortran-lang/test-drive"
    url = "https://github.com/fortran-lang/test-drive/releases/download/v0.4.0/test-drive-0.4.0.tar.xz"

    maintainers("awvwgk")

    license("Apache-2.0")

    version("0.4.0", "effabe5d46ea937a79f3ea8d37eea43caf38f9f1377398bad0ca02784235e54a")

    depends_on("fortran", type="build")  # generated

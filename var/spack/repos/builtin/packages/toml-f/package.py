# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TomlF(MesonPackage):
    """
    TOML parser implementation for data serialization and deserialization in Fortran
    """

    homepage = "https://toml-f.readthedocs.io"
    url = "https://github.com/toml-f/toml-f/releases/download/v0.3.1/toml-f-0.3.1.tar.xz"
    git = "https://github.com/toml-f/toml-f.git"

    maintainers("awvwgk")

    license("Apache-2.0")

    version("main", branch="main")
    version("0.3.1", sha256="7f40f60c8d9ffbb1b99fb051a3e6682c7dd04d7479aa1cf770eff8174b02544f")
    version("0.3.0", sha256="40ceca008091607165a09961b79312abfdbbda71cbb94a9dc2625b88c93ff45a")
    version("0.2.4", sha256="ebfeb1e201725b98bae3e656bde4eea2db90154efa8681de758f1389fec902cf")
    version("0.2.3", sha256="2dca7ff6d3e35415cd92454c31560d2b656c014af8236be09c54c13452e4539c")

    depends_on("fortran", type="build")  # generated

    depends_on("meson@0.57.2:", type="build")

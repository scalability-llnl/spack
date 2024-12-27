# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OxideRs(CargoPackage):
    """The Oxide CLI"""

    homepage = "https://github.com/oxidecomputer/oxide.rs"
    git = "https://github.com/oxidecomputer/oxide.rs.git"

    maintainers("alecbcs")

    license("MPL-2.0", checked_by="alecbcs")

    version("0.9.0", tag="v0.9.0+20241204.0.0", commit="cb25407df4e8bb4f33eb3b110d271cd8cd6dc16d")

    build_directory = "cli"

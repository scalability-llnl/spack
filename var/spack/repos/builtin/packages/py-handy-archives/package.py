# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHandyArchives(PythonPackage):
    """Some handy archive helpers for Python."""

    homepage = "https://github.com/domdfcoding/handy-archives"
    pypi = "handy_archives/handy_archives-0.2.0.tar.gz"

    license("MIT")

    version("0.2.0", sha256="fba21101fd9e29d5e3b72823261aaae06b9350686f0d2067786d64dce73eb3f6")

    depends_on("py-flit-core@3.2:3", type="build")

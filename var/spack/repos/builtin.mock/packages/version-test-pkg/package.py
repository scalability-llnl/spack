# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class VersionTestPkg(AutotoolsPackage):
    """Mock AutotoolsPackage to check proper version
    selection by clingo.
    """

    homepage = "https://www.gnu.org/software/make/"
    url = "http://www.example.com/libtool-version-1.0.tar.gz"

    version(
        "develop",
        git="https://git.savannah.gnu.org/git/libtool.git",
        branch="master",
        submodules=True,
    )
    version("2.4.6", sha256="e40b8f018c1da64edd1cc9a6fce5fa63b2e707e404e20cad91fbae337c98a5b7")

    depends_on("version-test-dependency-preferred", when="@develop")

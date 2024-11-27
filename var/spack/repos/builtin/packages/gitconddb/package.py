# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gitconddb(CMakePackage):
    """Conditions Database library using a Git repository as the
    storage backend"""

    homepage = "https://gitlab.cern.ch/lhcb/GitCondDB"
    url = "https://gitlab.cern.ch/lhcb/GitCondDB/-/archive/0.1.1/GitCondDB-0.1.1.tar.gz"
    git = "https://gitlab.cern.ch/lhcb/GitCondDB.git"

    maintainers("drbenmorgan")

    license("Apache-2.0")

    version("master", branch="master")
    version("0.2.0", sha256="dfbaa33581d5c6fac1102668c542b32d14499a30a2793bc55b133aba9f7295fc")
    version("0.1.3", sha256="29ed88498fd7ea3fd24bc80e9bfdec796cbeb584796c94c6c6b0baa368842ad4")
    version("0.1.2", sha256="121ac34d8afffbd97b052cbb10f15e78cef962fe25ded85d88ab26e1677b72b5")
    version("0.1.1", sha256="024a6867722a3a622ed4327ea7d15641dd48e4e8411bdcc21915e406b3c479a2")

    depends_on("cxx", type="build")  # generated

    # Add the cxxstd variant for forward compatibility, though we require 17
    _cxxstd_values = ("17",)
    variant(
        "cxxstd",
        default="17",
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake@3.10:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("nlohmann-json@3.2.0:", type="build")
    depends_on("googletest@1.8.1:", type="build")

    for s in _cxxstd_values:
        depends_on("fmt@5.2.0: cxxstd=" + s, when="cxxstd=" + s)
        # Maybe also a boost dependency for macOS older than catalina

    depends_on("libgit2")

    # Known conflicts on C++17 compatibility (aggressive for now)
    conflicts("%gcc@:7.9", msg="GitCondDB requires GCC 8 or newer for C++17 support")
    conflicts("%apple-clang", when="@:0.1", msg="No Darwin support for clang in older versions")
    conflicts(
        "%clang platform=darwin", when="@:0.1", msg="No Darwin support for clang in older versions"
    )

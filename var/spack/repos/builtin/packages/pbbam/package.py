# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pbbam(MesonPackage):
    """The pbbam software package provides components to create, query,
    & edit PacBio BAM files and associated indices.
    These components include a core C++ library,
    bindings for additional languages, and command-line utilities."""

    homepage = "https://github.com/PacificBiosciences/pbbam"
    url = "https://github.com/PacificBiosciences/pbbam/archive/refs/tags/0.18.0.tar.gz"
    maintainers("snehring")

    version(
        "2.1.0",
        sha256="605944f09654d964ce12c31d67e6766dfb1513f730ef5d4b74829b2b84dd464f",
        url="https://github.com/PacificBiosciences/pbbam/archive/refs/tags/v2.1.0.tar.gz",
    )
    version("0.18.0", sha256="45286e5f7deb7ff629e0643c8a416155915aec7b85d54c60b5cdc07f4d7b234a")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("boost@1.55.0:")
    depends_on("htslib@1.3.1:")
    # newer versions require C17
    conflicts("%gcc@:7.5.0", when="@2.1.0:")
    conflicts("%clang@:6.0.1", when="@2.1.0:")

    def meson_args(self):
        options = []
        if self.run_tests:
            options.append("-Dtests=true")
        else:
            options.append("-Dtests=false")

        return options

    def setup_build_environment(self, env):
        env.set("BOOST_ROOT", self.spec["boost"].prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("PacBioBAM_LIBRARIES", self.prefix.lib)
        env.set("PacBioBAM_INCLUDE_DIRS", self.prefix.include)

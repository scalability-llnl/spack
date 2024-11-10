# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Lazyten(CMakePackage):
    """Lightweight linear algebra library based on lazy matrices"""

    homepage = "https://lazyten.org"
    url = "https://github.com/lazyten/lazyten/archive/v0.4.1.tar.gz"
    git = "https://github.com/lazyten/lazyten.git"

    maintainers("mfherbst")

    license("GPL-3.0-only")

    #
    # Versions
    #
    version("develop", branch="master")
    version("0.4.1", sha256="696d151382993c13d04516c77db3ea712a70e3cb449539b9e79abc78cf245ae4")

    depends_on("cxx", type="build")  # generated

    #
    # Variants
    #
    # Library build type
    variant(
        "build_type",
        default="DebugRelease",
        description="The build type to build",
        values=("Debug", "Release", "DebugRelease"),
    )
    variant("shared", default=True, description="Build shared libraries (else the static one)")

    # Features
    variant("arpack", default=True, description="Build with Arpack support")

    # Components
    variant("examples", default=False, description="Compile examples")

    #
    # Conflicts
    #
    # Only builds on clang > 3.5 and gcc > 4.8
    conflicts("%intel", msg="krims only builds with gcc and clang")
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.5")

    #
    # Dependencies
    #
    depends_on("cmake@3:", type="build")

    depends_on("krims@develop", when="@develop")
    depends_on("krims@0.2.1", when="@0.4.1")

    depends_on("blas")
    depends_on("lapack")
    depends_on("armadillo@4:")
    depends_on("arpack-ng", when="+arpack")

    #
    # Settings and cmake cache
    #
    def cmake_args(self):
        spec = self.spec

        args = [
            "-DAUTOCHECKOUT_MISSING_REPOS=OFF",
            #
            "-DBUILD_SHARED_LIBS=" + str(spec.satisfies("+shared")),
            # TODO Hard-disable tests for now, since rapidcheck not in Spack
            "-DLAZYTEN_ENABLE_TESTS=OFF",
            "-DLAZYTEN_ENABLE_EXAMPLES=" + str(spec.satisfies("+examples")),
        ]

        # Tell lazyten where to look for the krims cmake config
        # and targets files
        krims_modules = os.path.join(spec["krims"].prefix.share, "cmake/krims")
        args.append("-Dkrims_DIR=" + krims_modules)

        # Add linear algebra backends
        lapack_blas = spec["lapack"].libs + spec["blas"].libs
        args.extend(
            [
                "-DARMADILLO_INCLUDE_DIR=" + spec["armadillo"].prefix.include,
                "-DARMADILLO_LIBRARY=" + ";".join(spec["armadillo"].libs),
                #
                "-DLAPACK_FOUND=ON",
                "-DLAPACK_LIBRARIES=" + ";".join(lapack_blas),
            ]
        )

        if spec.satisfies("+arpack"):
            args.append("-DARPACK_DIR=" + spec["arpack-ng"].prefix)
            args.append("-DARPACK_LIBRARY=" + ";".join(spec["arpack-ng"].libs))

        return args

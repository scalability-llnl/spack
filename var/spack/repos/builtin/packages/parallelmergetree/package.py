# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parallelmergetree(CMakePackage):
    """A multi-runtime implementation of a distributed merge tree
    segmentation algorithm. The implementation relies on the framework
    BabelFlow, which allows to execute the algorithm on different runtime
    systems."""

    homepage = "https://bitbucket.org/cedmav/parallelmergetree"
    git = "https://bitbucket.org/cedmav/parallelmergetree.git"

    maintainers("spetruzza")

    version(
        "1.1.2",
        git="https://bitbucket.org/cedmav/parallelmergetree.git",
        tag="v1.1.2",
        commit="22ec85177a66b3850ec3aa8ae73da4ad187f6156",
        submodules=True,
    )

    version(
        "1.1.1",
        git="https://bitbucket.org/cedmav/parallelmergetree.git",
        tag="v1.1.1",
        commit="d4b56978dd1b9c9d62d5dd3a0caadfc3102bdf42",
        submodules=True,
    )

    version(
        "1.1.0",
        git="https://bitbucket.org/cedmav/parallelmergetree.git",
        tag="v1.1.0",
        commit="4a5a81b2c857eda9599f257de8719f68f31a5900",
        submodules=True,
    )

    version(
        "1.0.2",
        git="https://bitbucket.org/cedmav/parallelmergetree.git",
        tag="v1.0.2",
        commit="c0b1f305d7f8e3d0bf7cffe22c1e2ac1c0faf05e",
        submodules=True,
    )

    version(
        "1.0.0",
        git="https://bitbucket.org/cedmav/parallelmergetree.git",
        tag="v1.0.0",
        commit="9cfb68fdf0f8e881a4bfd94ae5d3ae25c9e01ea6",
        submodules=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("babelflow@1.1.0", when="@1.1.2")
    depends_on("babelflow@1.1.0", when="@1.1.1")
    depends_on("babelflow@1.1.0", when="@1.1.0")
    depends_on("babelflow@1.0.1", when="@1.0.2")

    variant("shared", default=True, description="Build ParallelMergeTree as shared libs")

    # The C++ headers of gcc-11 don't provide <algorithm> as side effect of others
    @when("%gcc@11:")
    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", "-include algorithm")

    def cmake_args(self):
        args = []

        if "+shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")

        args.append("-DLIBRARY_ONLY=ON")
        args.append("-DBabelFlow_DIR={0}".format(self.spec["babelflow"].prefix))

        return args

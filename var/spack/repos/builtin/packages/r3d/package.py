# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class R3d(CMakePackage):
    """Fast, robust polyhedral intersections, analytic integration, and
    conservative voxelization."""

    homepage = "https://github.com/devonmpowell/r3d"
    git = "https://github.com/devonmpowell/r3d.git"

    maintainers("raovgarimella", "gaber")

    version("master", branch="master")
    version("2021-03-16", commit="5978a3f9cc145a52eecbf89c44d7fd2166b4c778")
    version("2019-04-24", commit="86cea79c124c6a8edd8c8cdea61e3e923acb0b22", deprecated=True)
    version("2018-12-19", commit="47308f68c782ed3227d3dab1eff24d41f6421f21", deprecated=True)
    version("2018-01-07", commit="d6799a582256a120ef3bd7e18959e96cba0e5495", deprecated=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "r3d_max_verts",
        default="0",
        description=(
            "Maximum number of vertices allowed in a polyhedron " "(versions 2021-03-10 or later)"
        ),
    )

    # Bypass CMake for older builds
    variant(
        "test",
        default=False,
        description="Build R3D regression tests (versions 2019-04-24 or earlier)",
    )

    variant(
        "pic", default=False, description="Produce position-independent code (for shared libs)"
    )

    @when("@:2019-04-24")
    def cmake(self, spec, prefix):
        pass

    @when("@:2019-04-24")
    def build(self, spec, prefix):
        make_args = ["CC={0}".format(spack_cc)]
        make("libr3d.a", *make_args)

        if "+test" in spec:
            with working_dir("tests"):
                make("all", *make_args)

    @when("@:2019-04-24")
    def install(self, spec, prefix):
        # R3D does not have an install target so create our own here.
        mkdirp(prefix.include)
        my_headers = find(".", "*.h", recursive=False)
        for my_header in my_headers:
            install(my_header, prefix.include)
        mkdirp(prefix.lib)
        install("libr3d.a", prefix.lib)

        if "+test" in spec:
            with working_dir("tests"):
                # R3D does not have an install target so create our own here.
                mkdirp(prefix.test)
                install("r2d_unit_tests", prefix.test)
                install("r3d_unit_tests", prefix.test)
                install("rNd_unit_tests", prefix.test)

    # CMake support was added in 2021-03-10
    @when("@2021-03-10:")
    def cmake_args(self):
        options = []
        r3d_max_verts = self.spec.variants["r3d_max_verts"].value
        if r3d_max_verts != "0":
            options.append("-DR3D_MAX_VERTS=" + r3d_max_verts)

        if self.run_tests:
            options.append("-DENABLE_UNIT_TESTS=ON")
        else:
            options.append("-DENABLE_UNIT_TESTS=OFF")

        options.append(self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"))

        return options

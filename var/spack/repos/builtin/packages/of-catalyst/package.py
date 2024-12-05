# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OfCatalyst(CMakePackage):
    """Of-catalyst is a library for OpenFOAM that provides a runtime-selectable
    function object for embedding ParaView Catalyst in-situ visualization
    into arbitrary OpenFOAM simulations.
    Supports in-situ conversion of the following types:
      1) finite volume meshes and fields, single or multi-region;
      2) finite area meshes and fields, single region;
      3) lagrangian (clouds), single or multiple clouds.
    This offering is part of the community repository supported by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    OpenCFD Ltd has been developing and releasing OpenFOAM since its debut
    in 2004.
    """

    # Currently only via git
    homepage = "https://develop.openfoam.com/Community/catalyst"
    git = "https://develop.openfoam.com/Community/catalyst.git"

    version("develop", branch="develop")
    version("1806", tag="v1806", commit="d97babec3581bad413fd602e17fcd4bc1e312d26")

    depends_on("cxx", type="build")  # generated

    variant("full", default=False, description="Build against paraview (full) or catalyst (light)")

    depends_on("openfoam@1806", when="@1806", type=("build", "link", "run"))
    depends_on("openfoam@develop", when="@develop", type=("build", "link", "run"))

    with when("+full"):
        depends_on("paraview@5.5: ~qt")
        depends_on("gl")
        requires("^[virtuals=gl] osmesa")

    root_cmakelists_dir = "src/catalyst"

    def cmake_args(self):
        """Populate cmake arguments for ParaView."""
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY:PATH=%s"
            % join_path(self.stage.source_path, "spack-build")
        ]

        return cmake_args

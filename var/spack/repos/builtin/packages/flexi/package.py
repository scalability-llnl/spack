# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flexi(CMakePackage):
    """Open Source High-Order Unstructured Discontinuous Galerkin Fluid
    Dynamics Solver"""

    homepage = "https://www.flexi-project.org/"
    git = "https://github.com/flexi-framework/flexi.git"

    license("GPL-3.0-or-later")

    version("master", preferred=True)
    version("21.03.0", tag="v21.03.0", commit="d061978e5d96cfc96c06edc1bae9d92cbe540c18")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("for_aarch64.patch", when="target=aarch64:")

    variant("mpi", default=True, description="Enable MPI")
    variant(
        "2d", default=False, description="If set to True the code will run in two-dimensional mode"
    )
    variant(
        "eqnsysname",
        default="navierstokes",
        values=("navierstokes", "linearscalaradvection", "rans_sa"),
        multi=False,
        description="Defines the equation system",
    )
    variant(
        "fv",
        default=False,
        description="Enables the usage of the finite volume subcell shock capturing mechanism",
    )
    variant(
        "lifting",
        default="br1",
        values=("br1", "br2"),
        multi=False,
        description=(
            "Two different lifting methods for the parabolic part of "
            "the equation system available"
        ),
    )
    variant(
        "nodetype",
        default="GAUSS",
        values=("GAUSS", "GAUSS-LOBATTO"),
        multi=False,
        description="Space discretization basis function",
    )
    variant(
        "split", default=False, description="Split form of the discontinuous Galerkin operator"
    )
    variant(
        "parabolic",
        default=True,
        description=(
            "Defines whether the parabolic part of the chosen system " "should be included or not"
        ),
    )
    variant(
        "testcase",
        default="default",
        values=("default", "taylorgreenvortex", "phill", "channel", "riemann2d"),
        multi=False,
        description="Defines the used test case",
    )
    variant(
        "viscosity",
        default="constant",
        values=("constant", "sutherland", "powerlaw"),
        multi=False,
        description="Defines modeling approach for viscosity",
    )
    variant("eddy_viscosity", default=False, description="Enable eddy viscosity")

    # Available Tools
    variant("visu", default=True, description="Enable posti_visu")
    variant("swapmesg", default=False, description="Enable posti_swapmesh")
    variant("preparerecordpoints", default=False, description="Enable posti_preparerecordpoints")
    variant(
        "visualizerecordpoints", default=False, description="Enable posti_visualizerecordpoints"
    )
    variant("evaluaterecordpoints", default=False, description="Enable posti_evaluaterecordpoints")
    variant("mergetimeaverages", default=False, description="Enable posti_mergetimeaverages")
    variant("channel_fft", default=False, description="Enable posti_channel_fft")
    variant("to3d", default=False, description="Enable posti_to3d")
    variant("avg2d", default=False, description="Enable posti_avg2d")

    conflicts("+to3d", when="@:21.03.0", msg="Only available in newer releases")
    conflicts("nodetype=GAUSS", when="+split", msg="Only available for Gauss-Lobatto nodes")

    depends_on("mpi", when="+mpi")
    depends_on("hdf5+fortran+mpi", when="+mpi")
    depends_on("hdf5+fortran~mpi", when="~mpi")
    depends_on("lapack")
    depends_on("zlib-api")
    depends_on("fftw", when="+channel_fft")

    def flag_handler(self, name, flags):
        if name == "fflags":
            if self.spec.satisfies("%gcc@10:"):
                if flags is None:
                    flags = []
                flags.append("-fallow-argument-mismatch")

        return (flags, None, None)

    def cmake_args(self):
        args = [
            "-DLIBS_BUILD_HDF5:BOOL=OFF",
            self.define_from_variant("LIBS_USE_MPI", "mpi"),
            self.define_from_variant("FLEXI_2D", "2d"),
            self.define_from_variant("FLEXI_EQNSYSNAME", "eqnsysname"),
            self.define_from_variant("FLEXI_FV", "fv"),
            self.define_from_variant("FLEXI_LIFTING", "lifting"),
            self.define_from_variant("FLEXI_NODETYPE", "nodetype"),
            self.define_from_variant("FLEXI_SPLIT_DG", "split"),
            self.define_from_variant("FLEXI_PARABOLIC", "parabolic"),
            self.define_from_variant("FLEXI_TESTCASE", "testcase"),
            self.define_from_variant("FLEXI_VISCOSITY", "viscosity"),
            self.define_from_variant("FLEXI_EDDYVISCOSITY", "eddy_viscosity"),
            self.define_from_variant("POSTI_VISU", "visu"),
            self.define_from_variant("POSTI_SWAPMESH", "swapmesg"),
            self.define_from_variant("POSTI_RP_VISUALIZE", "visualizerecordpoints"),
            self.define_from_variant("POSTI_RP_EVALUATE", "evaluaterecordpoints"),
            self.define_from_variant("POSTI_MERGETIMEAVERAGES", "mergetimeaverages"),
            self.define_from_variant("POSTI_CHANNEL_FFT", "channel_fft"),
            self.define_from_variant("POSTI_TO3D", "to3d"),
            self.define_from_variant("POSTI_AVG2D", "avg2d"),
        ]

        if self.spec.satisfies("@:21.03.0"):
            args.append(self.define_from_variant("POSTI_RP_PREPARERE", "preparerecordpoints"))
        else:
            args.append(self.define_from_variant("POSTI_RP_PREPARE", "preparerecordpoints"))

        return args

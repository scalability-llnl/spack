# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import re
import sys

from spack.build_environment import dso_suffix
from spack.error import NoHeadersError
from spack.operating_systems.mac_os import macos_version
from spack.package import *
from spack.pkg.builtin.kokkos import Kokkos

# Trilinos is complicated to build, as an inspiration a couple of links to
# other repositories which build it:
# https://github.com/hpcugent/easybuild-easyblocks/blob/master/easybuild/easyblocks/t/trilinos.py#L111
# https://github.com/koecher/candi/blob/master/deal.II-toolchain/packages/trilinos.package
# https://gitlab.com/configurations/cluster-config/blob/master/trilinos.sh
# https://github.com/Homebrew/homebrew-science/blob/master/trilinos.rb and some
# relevant documentation/examples:
# https://github.com/trilinos/Trilinos/issues/175


class Trilinos(CMakePackage, CudaPackage, ROCmPackage):
    """The Trilinos Project is an effort to develop algorithms and enabling
    technologies within an object-oriented software framework for the solution
    of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """

    homepage = "https://trilinos.org/"
    url = "https://github.com/trilinos/Trilinos/archive/refs/tags/trilinos-release-12-12-1.tar.gz"
    git = "https://github.com/trilinos/Trilinos.git"

    maintainers("keitat", "kuberry", "jwillenbring", "psakievich")

    tags = ["e4s"]

    # ###################### Versions ##########################

    version("master", branch="master")
    version("develop", branch="develop")
    version("16.0.0", sha256="46bfc40419ed2aa2db38c144fb8e61d4aa8170eaa654a88d833ba6b92903f309")
    version("15.1.1", sha256="2108d633d2208ed261d09b2d6b2fbae7a9cdc455dd963c9c94412d38d8aaefe4")
    version("15.0.0", sha256="5651f1f967217a807f2c418a73b7e649532824dbf2742fa517951d6cc11518fb")
    version("14.4.0", sha256="8e7d881cf6677aa062f7bfea8baa1e52e8956aa575d6a4f90f2b6f032632d4c6")
    version("14.2.0", sha256="c96606e5cd7fc9d25b9dc20719cd388658520d7cbbd2b4de77a118440d1e0ccb")
    version("14.0.0", sha256="054d2fabdf70fce0dfaeb20eed265bd7894045d3e00c3d1ddb72d1c77c339ca1")
    version("13.4.1", sha256="5465cbff3de7ef4ac7d40eeff9d99342c00d9d20eee0a5f64f0a523093f5f1b3")
    version("13.4.0", sha256="39550006e059043b7e2177f10467ae2f77fe639901aee91cbc1e359516ff8d3e")
    version("13.2.0", sha256="0ddb47784ba7b8a6b9a07a4822b33be508feb4ccd54301b2a5d10c9e54524b90")
    version("13.0.1", sha256="0bce7066c27e83085bc189bf524e535e5225636c9ee4b16291a38849d6c2216d")
    version("13.0.0", sha256="d44e8181b3ef5eae4e90aad40a33486f0b2ae6ba1c34b419ce8cbc70fd5dd6bd")
    version(
        "12.18.1", commit="55a75997332636a28afc9db1aee4ae46fe8d93e7"
    )  # tag trilinos-release-12-8-1
    version("12.14.1", sha256="52a4406cca2241f5eea8e166c2950471dd9478ad6741cbb2a7fc8225814616f0")
    version("12.12.1", sha256="5474c5329c6309224a7e1726cf6f0d855025b2042959e4e2be2748bd6bb49e18")
    version("12.10.1", sha256="ab81d917196ffbc21c4927d42df079dd94c83c1a08bda43fef2dd34d0c1a5512")
    version("12.8.1", sha256="d20fe60e31e3ba1ef36edecd88226240a518f50a4d6edcc195b88ee9dda5b4a1")
    version("12.6.4", sha256="1c7104ba60ee8cc4ec0458a1c4f6a26130616bae7580a7b15f2771a955818b73")
    version("12.6.3", sha256="4d28298bb4074eef522db6cd1626f1a934e3d80f292caf669b8846c0a458fe81")
    version("12.6.2", sha256="8be7e3e1166cc05aea7f856cc8033182e8114aeb8f87184cb38873bfb2061779")
    version("12.6.1", sha256="4b38ede471bed0036dcb81a116fba8194f7bf1a9330da4e29c3eb507d2db18db")
    version("12.4.2", sha256="fd2c12e87a7cedc058bcb8357107ffa2474997aa7b17b8e37225a1f7c32e6f0e")
    version("12.2.1", sha256="088f303e0dc00fb4072b895c6ecb4e2a3ad9a2687b9c62153de05832cf242098")
    version("12.0.1", sha256="eee7c19ca108538fa1c77a6651b084e06f59d7c3307dae77144136639ab55980")
    version("11.14.3", sha256="e37fa5f69103576c89300e14d43ba77ad75998a54731008b25890d39892e6e60")
    version("11.14.2", sha256="f22b2b0df7b88e28b992e19044ba72b845292b93cbbb3a948488199647381119")
    version("11.14.1", sha256="f10fc0a496bf49427eb6871c80816d6e26822a39177d850cc62cf1484e4eec07")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+fortran")

    # ###################### Variants ##########################

    # Build options
    variant("complex", default=False, description="Enable complex numbers in Trilinos")
    variant(
        "cuda_constexpr",
        default=False,
        description="Enable relaxed constexpr functions for CUDA build",
    )
    variant("cuda_rdc", default=False, description="Turn on RDC for CUDA build")
    variant("rocm_rdc", default=False, description="Turn on RDC for ROCm build")
    variant(
        "cxxstd", default="14", description="C++ standard", values=["11", "14", "17"], multi=False
    )
    variant("debug", default=False, description="Enable runtime safety and debug checks")
    variant(
        "explicit_template_instantiation",
        default=True,
        description="Enable explicit template instantiation (ETI)",
    )
    variant(
        "float", default=False, description="Enable single precision (float) numbers in Trilinos"
    )
    variant("fortran", default=True, description="Compile with Fortran support")
    variant(
        "gotype",
        default="long_long",
        values=("int", "long", "long_long", "all"),
        multi=False,
        description="global ordinal type for Tpetra",
    )
    variant("openmp", default=False, description="Enable OpenMP")
    variant("python", default=False, when="@15:", description="Build PyTrilinos2 wrappers")
    variant("python", default=False, when="@:14", description="Build PyTrilinos wrappers")
    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("uvm", default=False, when="@13.2: +cuda", description="Turn on UVM for CUDA build")
    variant("wrapper", default=False, description="Use nvcc-wrapper for CUDA build")

    # Makes the Teuchos Memory Management classes (Teuchos::RCP, Teuchos::Ptr, Teuchos::Array,
    # Teuchos::ArrayView, and Teuchos::ArrayRCP) thread-safe. Requires at least the OMP kokkos
    # backend to be enabled. Without, this seemingly does nothing
    variant(
        "threadsafe", default=False, when="+openmp", description="Enable threadsafe in Teuchos"
    )

    # TPLs (alphabet order)
    variant("adios2", default=False, description="Enable ADIOS2")
    variant("boost", default=False, description="Compile with Boost")
    variant("hdf5", default=False, description="Compile with HDF5")
    variant("hypre", default=False, description="Compile with Hypre preconditioner")
    variant("mpi", default=True, description="Compile with MPI parallelism")
    variant("mumps", default=False, description="Compile with support for MUMPS solvers")
    variant("suite-sparse", default=False, description="Compile with SuiteSparse solvers")
    variant("superlu-dist", default=False, description="Compile with SuperluDist solvers")
    variant("superlu", default=False, description="Compile with SuperLU solvers")
    variant("strumpack", default=False, description="Compile with STRUMPACK solvers")
    variant("x11", default=False, description="Compile with X11 when +exodus")

    # Package options (alphabet order)
    variant("adelus", default=False, description="Compile with Adelus")
    variant("amesos", default=True, description="Compile with Amesos")
    variant("amesos2", default=True, description="Compile with Amesos2")
    variant("anasazi", default=True, description="Compile with Anasazi")
    variant("aztec", default=True, description="Compile with Aztec")
    variant("belos", default=True, description="Compile with Belos")
    variant("chaco", default=False, description="Compile with Chaco from SEACAS")
    variant("epetra", default=True, description="Compile with Epetra")
    variant("epetraext", default=True, description="Compile with EpetraExt")
    variant("exodus", default=False, description="Compile with Exodus from SEACAS")
    variant("ifpack", default=True, description="Compile with Ifpack")
    variant("ifpack2", default=True, description="Compile with Ifpack2")
    variant("intrepid", default=False, description="Enable Intrepid")
    variant("intrepid2", default=False, description="Enable Intrepid2")
    variant("isorropia", default=False, description="Compile with Isorropia")
    variant("gtest", default=False, description="Build vendored Googletest")
    variant("kokkos", default=True, description="Compile with Kokkos")
    variant("ml", default=True, description="Compile with ML")
    variant("minitensor", default=False, description="Compile with MiniTensor")
    variant("muelu", default=True, description="Compile with Muelu")
    variant("nox", default=False, description="Compile with NOX")
    variant("pamgen", default=False, description="Compile with Pamgen")
    variant("panzer", default=False, description="Compile with Panzer")
    variant("piro", default=False, description="Compile with Piro")
    variant("phalanx", default=False, description="Compile with Phalanx")
    variant("rol", default=False, description="Compile with ROL")
    variant("rythmos", default=False, description="Compile with Rythmos")
    variant("sacado", default=True, description="Compile with Sacado")
    variant("stk", default=False, description="Compile with STK")
    variant("shards", default=False, description="Compile with Shards")
    variant("shylu", default=False, description="Compile with ShyLU")
    variant("stokhos", default=False, description="Compile with Stokhos")
    variant("stratimikos", default=False, description="Compile with Stratimikos")
    variant("teko", default=False, description="Compile with Teko")
    variant("tempus", default=False, description="Compile with Tempus")
    variant("test", default=False, description="Enable testing")
    variant("thyra", default=False, description="Compile with Thyra")
    variant("tpetra", default=True, description="Compile with Tpetra")
    variant("trilinoscouplings", default=False, description="Compile with TrilinosCouplings")
    variant("zoltan", default=False, description="Compile with Zoltan")
    variant("zoltan2", default=False, description="Compile with Zoltan2")

    # Internal package options (alphabetical order)
    variant("basker", default=False, description="Compile with the Basker solver in Amesos2")
    variant("epetraextbtf", default=False, description="Compile with BTF in EpetraExt")
    variant(
        "epetraextexperimental",
        default=False,
        description="Compile with experimental in EpetraExt",
    )
    variant(
        "epetraextgraphreorderings",
        default=False,
        description="Compile with graph reorderings in EpetraExt",
    )

    # External package options
    variant("dtk", default=False, description="Enable DataTransferKit (deprecated)")
    variant("scorec", default=False, description="Enable SCOREC")
    variant("mesquite", default=False, description="Enable Mesquite (deprecated)")

    resource(
        name="dtk",
        git="https://github.com/ornl-cees/DataTransferKit.git",
        commit="4fe4d9d56cfd4f8a61f392b81d8efd0e389ee764",  # branch dtk-3.0
        placement="DataTransferKit",
        when="+dtk @12.14.0:12.14",
    )
    resource(
        name="dtk",
        git="https://github.com/ornl-cees/DataTransferKit.git",
        commit="edfa050cd46e2274ab0a0b7558caca0079c2e4ca",  # tag 3.1-rc1
        placement="DataTransferKit",
        submodules=True,
        when="+dtk @12.18.0:12.18",
    )
    resource(
        name="scorec",
        git="https://github.com/SCOREC/core.git",
        commit="73c16eae073b179e45ec625a5abe4915bc589af2",  # tag v2.2.5
        placement="SCOREC",
        when="+scorec",
    )
    resource(
        name="mesquite",
        url="https://github.com/trilinos/mesquite/archive/trilinos-release-12-12-1.tar.gz",
        sha256="e0d09b0939dbd461822477449dca611417316e8e8d8268fd795debb068edcbb5",
        placement="packages/mesquite",
        when="+mesquite @12.12.1:12.16",
    )
    resource(
        name="mesquite",
        git="https://github.com/trilinos/mesquite.git",
        commit="20a679679b5cdf15bf573d66c5dc2b016e8b9ca1",  # branch trilinos-release-12-12-1
        placement="packages/mesquite",
        when="+mesquite @12.18.1:12.18",
    )
    resource(
        name="mesquite",
        git="https://github.com/trilinos/mesquite.git",
        tag="develop",
        placement="packages/mesquite",
        when="+mesquite @master",
    )

    # ###################### Conflicts ##########################

    # Epetra stack
    with when("~epetra"):
        conflicts("+amesos")
        conflicts("+aztec")
        conflicts("+epetraext")
        conflicts("+ifpack")
        conflicts("+isorropia")
        conflicts("+ml", when="@13.2:")
    with when("~epetraext"):
        conflicts("+isorropia")
        conflicts("+teko")
        conflicts("+epetraextbtf")
        conflicts("+epetraextexperimental")
        conflicts("+epetraextgraphreorderings")
    with when("+teko"):
        conflicts("~ml")
        conflicts("~stratimikos")
        conflicts("@:12 gotype=long")
    with when("+piro"):
        conflicts("~stratimikos")
        conflicts("~thyra")
        conflicts("~tpetra")
        conflicts("@15: ~teko")
        conflicts("~nox")

    # Tpetra stack
    with when("~kokkos"):
        conflicts("+cuda")
        conflicts("+rocm")
        conflicts("+tpetra")
        conflicts("+intrepid2")
        conflicts("+phalanx")
    with when("~tpetra"):
        conflicts("+amesos2")
        conflicts("+dtk")
        conflicts("+ifpack2")
        conflicts("+muelu")
        conflicts("+teko")
        conflicts("+zoltan2")

    with when("~zoltan"):
        conflicts("+isorropia")
        conflicts("+scorec")
        conflicts("+shylu")
        conflicts("+zoltan2")
    with when("~shards"):
        conflicts("+intrepid")
        conflicts("+intrepid2")
        conflicts("+scorec")
        conflicts("+stk")
    with when("+scorec"):
        conflicts("~mpi")
        conflicts("~stk")

    # Panzer is not gen-2 library
    with when("+panzer"):
        conflicts("~intrepid2")
        conflicts("~mpi")
        conflicts("~phalanx")
        conflicts("~sacado")
        conflicts("~tpetra")
        conflicts("~thyra")
        conflicts("~zoltan")
        conflicts("~nox")
        conflicts("~rythmos")
        conflicts("~piro")
        conflicts("~stratimikos")
        conflicts("~stk")
        conflicts("~ml")
        conflicts("~ifpack")
        conflicts("~aztec")

    with when("+tempus"):
        conflicts("~nox")
        conflicts("~thyra")

    # Known requirements from tribits dependencies
    conflicts("~thyra", when="+stratimikos")
    conflicts("+adelus", when="~kokkos")
    conflicts("+aztec", when="~fortran")
    conflicts("+basker", when="~amesos2")
    conflicts("+ifpack2", when="~belos")
    conflicts("+intrepid", when="~sacado")
    conflicts("+minitensor", when="~boost")
    conflicts("+phalanx", when="~sacado")
    conflicts("+stokhos", when="~kokkos")

    # Only allow DTK with Trilinos 12.14, 12.18
    conflicts("+dtk", when="~boost")
    conflicts("+dtk", when="~intrepid2")
    conflicts("+dtk", when="@:12.12,13:")

    # Installed FindTrilinos are broken in SEACAS if Fortran is disabled
    # see https://github.com/trilinos/Trilinos/issues/3346
    conflicts("+exodus", when="@:13.0.1 ~fortran")
    # Only allow Mesquite with Trilinos 12.12 and up, and master
    conflicts("+mesquite", when="@:12.10,master")
    # Strumpack is only available as of mid-2021
    conflicts("+strumpack", when="@:13.0")
    # Can only use one type of SuperLU
    conflicts("+superlu-dist", when="+superlu")
    # Amesos and Ifpack only support up to SuperLU 4.x.y interfaces
    conflicts("+amesos", when="+superlu@5:")
    conflicts("+ifpack", when="+superlu@5:")
    # For Trilinos v11 we need to force SuperLUDist=OFF, since only the
    # deprecated SuperLUDist v3.3 together with an Amesos patch is working.
    conflicts("+superlu-dist", when="@11.4.1:11.14.3")
    # see https://github.com/trilinos/Trilinos/issues/3566
    conflicts(
        "+superlu-dist", when="+float+amesos2+explicit_template_instantiation^superlu-dist@5.3.0:"
    )
    # Amesos, conflicting types of double and complex SLU_D
    # see https://trilinos.org/pipermail/trilinos-users/2015-March/004731.html
    # and https://trilinos.org/pipermail/trilinos-users/2015-March/004802.html
    conflicts("+superlu-dist", when="+complex+amesos2")
    conflicts("+adios2", when="@:12.14.1")
    conflicts("cxxstd=11", when="@13.2:")
    conflicts("cxxstd=14", when="@14:")
    conflicts("cxxstd=17", when="@:12")
    conflicts("cxxstd=11", when="+wrapper ^cuda@6.5.14")
    conflicts("cxxstd=14", when="+wrapper ^cuda@6.5.14:8.0.61")
    conflicts("cxxstd=17", when="+wrapper ^cuda@6.5.14:10.2.89")

    # Multi-value gotype only applies to trilinos through 12.14
    conflicts("gotype=all", when="@12.15:")

    # CUDA without wrapper requires clang
    requires(
        "%clang",
        when="+cuda~wrapper",
        msg="trilinos~wrapper+cuda can only be built with the Clang compiler",
    )
    conflicts("+cuda_rdc", when="~cuda")
    conflicts("+rocm_rdc", when="~rocm")
    conflicts("+wrapper", when="~cuda")
    conflicts("+wrapper", when="%clang")

    # Old trilinos fails with new CUDA (see #27180)
    conflicts("@:13.0.1 +cuda", when="^cuda@11:")
    # Build hangs with CUDA 11.6 (see #28439)
    conflicts("+cuda +stokhos", when="^cuda@11.6:")
    # superlu-dist defines a macro EMPTY which conflicts with a header in cuda
    # used when building stokhos
    # Fix: https://github.com/xiaoyeli/superlu_dist/commit/09cb1430f7be288fd4d75b8ed461aa0b7e68fefe
    # is not tagged yet. See discussion here https://github.com/trilinos/Trilinos/issues/11839
    conflicts("+cuda +stokhos +superlu-dist")

    # stokhos fails on xl/xl_r
    conflicts("+stokhos", when="%xl")
    conflicts("+stokhos", when="%xl_r")

    # Current Windows support, only have serial static builds
    conflicts(
        "+shared",
        when="platform=windows",
        msg="Only static builds are supported on Windows currently.",
    )
    conflicts(
        "+mpi",
        when="platform=windows",
        msg="Only serial builds are supported on Windows currently.",
    )

    # ###################### Dependencies ##########################

    # External Kokkos
    depends_on("kokkos@4.4.01", when="@master: +kokkos")
    depends_on("kokkos@4.3.01", when="@16.0.0 +kokkos")
    depends_on("kokkos@4.2.01", when="@15.1.0:15.1.1 +kokkos")
    depends_on("kokkos@4.1.00", when="@14.4.0:15.0.0 +kokkos")

    depends_on("kokkos +wrapper", when="trilinos@14.4.0: +kokkos +wrapper")
    depends_on("kokkos ~wrapper", when="trilinos@14.4.0: +kokkos ~wrapper")

    for a in CudaPackage.cuda_arch_values:
        arch_str = "+cuda cuda_arch={0}".format(a)
        kokkos_spec = "kokkos {0}".format(arch_str)
        depends_on(kokkos_spec, when="@14.4.0: +kokkos {0}".format(arch_str))

    for a in ROCmPackage.amdgpu_targets:
        arch_str = "+rocm amdgpu_target={0}".format(a)
        kokkos_spec = "kokkos {0}".format(arch_str)
        depends_on(kokkos_spec, when="@14.4.0: +kokkos {0}".format(arch_str))

    depends_on("adios2", when="+adios2")
    depends_on("binder@1.3:", when="@15: +python", type="build")
    depends_on("blas")
    depends_on("boost+graph+math+exception+stacktrace", when="+boost")
    depends_on("boost+graph+math+exception+stacktrace", when="@:13.4.0 +stk")
    depends_on("cgns", when="+exodus")
    depends_on("cmake@3.23:", type="build", when="@14.0.0:")
    depends_on("hdf5+hl", when="+hdf5")
    for plat in ["darwin", "linux"]:
        depends_on("hypre~internal-superlu~int64", when="+hypre platform=%s" % plat)
    depends_on("hypre-cmake~int64", when="+hypre platform=windows")
    depends_on("kokkos-nvcc-wrapper", when="+wrapper")
    depends_on("lapack")
    # depends_on('perl', type=('build',)) # TriBITS finds but doesn't use...
    depends_on("libx11", when="+x11")
    depends_on("matio", when="+exodus")
    depends_on("metis", when="+zoltan")
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="@15: +python")
    depends_on("netcdf-c", when="+exodus")
    depends_on("parallel-netcdf", when="+exodus+mpi")
    depends_on("parmetis", when="+mpi +zoltan")
    depends_on("parmetis", when="+scorec")
    depends_on("py-mpi4py", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-pybind11", when="@15: +python", type=("build", "link"))
    depends_on("python", when="+python")
    depends_on("python", when="@13.2: +ifpack +hypre", type="build")
    depends_on("python", when="@13.2: +ifpack2 +hypre", type="build")
    depends_on("scalapack", when="+mumps")
    depends_on("scalapack", when="+strumpack+mpi")
    depends_on("strumpack+shared", when="+strumpack")
    depends_on("suite-sparse@:7.3.1", when="+suite-sparse")
    depends_on("superlu-dist", when="+superlu-dist")
    depends_on("superlu@3:5.2", when="@12.18.1: +superlu")
    depends_on("superlu@3:5.1.1", when="@12.14.1 +superlu")
    depends_on("superlu@3:4", when="@:12.12.1 +superlu")
    depends_on("swig", when="@:14 +python")
    depends_on("zlib-api", when="+zoltan")

    # Trilinos' Tribits config system is limited which makes it very tricky to
    # link Amesos with static MUMPS, see
    # https://trilinos.org/docs/dev/packages/amesos2/doc/html/classAmesos2_1_1MUMPS.html
    # One could work it out by getting linking flags from mpif90 --showme:link
    # (or alike) and adding results to -DTrilinos_EXTRA_LINK_FLAGS together
    # with Blas and Lapack and ScaLAPACK and Blacs and -lgfortran and it may
    # work at the end. But let's avoid all this by simply using shared libs
    depends_on("mumps@5.0:+shared", when="+mumps")

    for _flag in ("~mpi", "+mpi"):
        depends_on("hdf5" + _flag, when="+hdf5" + _flag)
        depends_on("mumps" + _flag, when="+mumps" + _flag)
    for _flag in ("~openmp", "+openmp"):
        depends_on("mumps" + _flag, when="+mumps" + _flag)

    depends_on("hwloc", when="@13: +kokkos")
    depends_on("hwloc+cuda", when="@13: +kokkos+cuda")
    depends_on("hypre@develop", when="@master: +hypre")
    depends_on("netcdf-c+mpi+parallel-netcdf", when="+exodus+mpi@12.12.1:")
    depends_on("superlu-dist@:4.3", when="@11.14.1:12.6.1+superlu-dist")
    depends_on("superlu-dist@4.4:5.3", when="@12.6.2:12.12.1+superlu-dist")
    depends_on("superlu-dist@5.4:6.2.0", when="@12.12.2:13.0.0+superlu-dist")
    depends_on("superlu-dist@6.3.0:7", when="@13.0.1:13.4.0 +superlu-dist")
    depends_on("superlu-dist@6.3.0:", when="@13.4.1:13 +superlu-dist")
    depends_on("superlu-dist@develop", when="@master: +superlu-dist")

    # ###################### Patches ##########################

    patch("shylu-node-optional.patch", when="@13:14.4.0 +shylu")

    patch("umfpack_from_suitesparse.patch", when="@11.14.1:12.8.1")
    for _compiler in ["xl", "xl_r", "clang"]:
        patch("xlf_seacas.patch", when="@12.10.1:12.12.1 %" + _compiler)
        patch("xlf_tpetra.patch", when="@12.12.1 %" + _compiler)
    patch("fix_clang_errors_12_18_1.patch", when="@12.18.1%clang")
    patch("cray_secas_12_12_1.patch", when="@12.12.1%cce")
    patch("cray_secas.patch", when="@12.14.1:12%cce")
    patch(
        "https://patch-diff.githubusercontent.com/raw/trilinos/Trilinos/pull/10545.patch?full_index=1",
        sha256="62272054f7cc644583c269e692c69f0a26af19e5a5bd262db3ea3de3447b3358",
        when="@:13.4 +complex",
    )

    # workaround an NVCC bug with c++14 (https://github.com/trilinos/Trilinos/issues/6954)
    # avoid calling deprecated functions with CUDA-11
    patch("fix_cxx14_cuda11.patch", when="@13.0.0:13.0.1 cxxstd=14 ^cuda@11:")
    patch(
        "0001-use-the-gcnArchName-inplace-of-gcnArch-as-gcnArch-is.patch",
        when="@15.0.0 ^hip@6.0 +rocm",
    )
    patch("cstdint_gcc13.patch", when="@13.4.0:13.4.1 %gcc@13.0.0:")

    # Allow building with +teko gotype=long
    patch(
        "https://github.com/trilinos/Trilinos/commit/b17f20a0b91e0b9fc5b1b0af3c8a34e2a4874f3f.patch?full_index=1",
        sha256="063a38f402439fa39fd8d57315a321e6510adcd04aec5400a88e744aaa60bc8e",
        when="@13.0.0:13.0.1 +teko gotype=long",
    )

    def flag_handler(self, name, flags):
        spec = self.spec
        is_cce = spec.satisfies("%cce")

        if name == "cxxflags":
            if "+mumps" in spec:
                # see https://github.com/trilinos/Trilinos/blob/master/packages/amesos/README-MUMPS
                flags.append("-DMUMPS_5_0")
            if "+stk platform=darwin" in spec:
                flags.append("-DSTK_NO_BOOST_STACKTRACE")
            if "+stk%intel" in spec:
                # Workaround for Intel compiler segfaults with STK and IPO
                flags.append("-no-ipo")
            if "+wrapper" in spec:
                flags.append("--expt-extended-lambda")
        elif name == "ldflags":
            if spec.satisfies("%cce@:14"):
                flags.append("-fuse-ld=gold")
            if spec.satisfies("platform=linux ~cuda"):
                # TriBITS explicitly links libraries against all transitive
                # dependencies, leading to O(N^2) library resolution. When
                # CUDA is enabled (possibly only with MPI as well) the linker
                # flag does not propagate correctly.
                flags.append("-Wl,--as-needed")
            elif spec.satisfies("+stk +shared platform=darwin"):
                flags.append("-Wl,-undefined,dynamic_lookup")

            # Fortran lib (assumes clang is built with gfortran!)
            if "+fortran" in spec and spec.compiler.name in ["gcc", "clang", "apple-clang"]:
                fc = Executable(self.compiler.fc)
                libgfortran = fc(
                    "--print-file-name", "libgfortran." + dso_suffix, output=str
                ).strip()
                # if libgfortran is equal to "libgfortran.<dso_suffix>" then
                # print-file-name failed, use static library instead
                if libgfortran == "libgfortran." + dso_suffix:
                    libgfortran = fc("--print-file-name", "libgfortran.a", output=str).strip()
                # -L<libdir> -lgfortran required for OSX
                # https://github.com/spack/spack/pull/25823#issuecomment-917231118
                flags.append("-L{0} -lgfortran".format(os.path.dirname(libgfortran)))

        if is_cce:
            return (None, None, flags)
        return (flags, None, None)

    def url_for_version(self, version):
        url = "https://github.com/trilinos/Trilinos/archive/refs/tags/trilinos-release-{0}.tar.gz"
        return url.format(version.dashed)

    def setup_dependent_run_environment(self, env, dependent_spec):
        if "+cuda" in self.spec:
            # currently Trilinos doesn't perform the memory fence so
            # it relies on blocking CUDA kernel launch. This is needed
            # in case the dependent app also run a CUDA backend via Trilinos
            env.set("CUDA_LAUNCH_BLOCKING", "1")

    def setup_dependent_package(self, module, dependent_spec):
        if "+wrapper" in self.spec:
            self.spec.kokkos_cxx = self.spec["kokkos-nvcc-wrapper"].kokkos_cxx
        else:
            self.spec.kokkos_cxx = spack_cxx

    def setup_build_environment(self, env):
        spec = self.spec
        if "+cuda" in spec and "+wrapper" in spec:
            if "+mpi" in spec:
                env.set("OMPI_CXX", spec["kokkos-nvcc-wrapper"].kokkos_cxx)
                env.set("MPICH_CXX", spec["kokkos-nvcc-wrapper"].kokkos_cxx)
                env.set("MPICXX_CXX", spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            else:
                env.set("CXX", spec["kokkos-nvcc-wrapper"].kokkos_cxx)

        if "+rocm" in spec:
            if "+mpi" in spec:
                env.set("OMPI_CXX", self.spec["hip"].hipcc)
                env.set("MPICH_CXX", self.spec["hip"].hipcc)
                env.set("MPICXX_CXX", self.spec["hip"].hipcc)
            else:
                env.set("CXX", self.spec["hip"].hipcc)
            if "+stk" in spec:
                # Using CXXFLAGS for hipcc which doesn't use flags in the spack wrappers
                env.set("CXXFLAGS", "-DSTK_NO_BOOST_STACKTRACE")

    def cmake_args(self):
        options = []

        spec = self.spec
        define = self.define
        define_from_variant = self.define_from_variant

        if self.spec.satisfies("@master: +kokkos"):
            with open(
                os.path.join(self.stage.source_path, "packages", "kokkos", "CMakeLists.txt")
            ) as f:
                all_txt = f.read()
            r = dict(
                re.findall(r".*set\s?\(\s?Kokkos_VERSION_(MAJOR|MINOR|PATCH)\s?(\d+)", all_txt)
            )
            kokkos_version_in_trilinos_source = Version(
                ".".join([r["MAJOR"], r["MINOR"], r["PATCH"].zfill(2)])
            )
            kokkos_version_specified = spec["kokkos"].version
            if kokkos_version_in_trilinos_source != kokkos_version_specified:
                raise InstallError(
                    "For Trilinos@[master,develop], ^kokkos version in spec must "
                    "match version in Trilinos source code. Specify ^kokkos@{0} ".format(
                        kokkos_version_in_trilinos_source
                    )
                    + "for trilinos@[master,develop] instead of ^kokkos@{0}.\n".format(
                        kokkos_version_specified
                    )
                    + "Trilinos recipe maintainers, please update the ^kokkos version range"
                )

        def _make_definer(prefix):
            def define_enable(suffix, value=None):
                key = prefix + suffix
                if value is None:
                    # Default to lower-case spec
                    value = suffix.lower()
                elif isinstance(value, bool):
                    # Explicit true/false
                    return define(key, value)
                return define_from_variant(key, value)

            return define_enable

        # Return "Trilinos_ENABLE_XXX" for spec "+xxx" or boolean value
        define_trilinos_enable = _make_definer("Trilinos_ENABLE_")
        # Same but for TPLs
        define_tpl_enable = _make_definer("TPL_ENABLE_")

        # #################### Base Settings #######################

        options.extend(
            [
                define("Trilinos_VERBOSE_CONFIGURE", False),
                define_from_variant("BUILD_SHARED_LIBS", "shared"),
                define_trilinos_enable("ALL_OPTIONAL_PACKAGES", False),
                define_trilinos_enable("ALL_PACKAGES", False),
                define_trilinos_enable("CXX11", True),
                define_trilinos_enable("DEBUG", "debug"),
                define_trilinos_enable("EXAMPLES", False),
                define_trilinos_enable("SECONDARY_TESTED_CODE", True),
                define_trilinos_enable("TESTS", False),
                define_trilinos_enable("Fortran"),
                define_trilinos_enable("OpenMP"),
                define_trilinos_enable(
                    "EXPLICIT_INSTANTIATION", "explicit_template_instantiation"
                ),
                define_from_variant("Trilinos_ENABLE_THREAD_SAFE", "threadsafe"),
            ]
        )

        if spec.version >= Version("15"):
            options.append(define_trilinos_enable("PyTrilinos2", "python"))
        else:
            options.append(define_trilinos_enable("PyTrilinos", "python"))

        if "+test" in spec:
            options.append(define_trilinos_enable("TESTS", True))
            options.append(define("BUILD_TESTING", True))
        else:
            options.append(define_trilinos_enable("TESTS", False))

        if spec.version >= Version("13"):
            options.append(define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        else:
            # Prior to version 13, Trilinos would erroneously inject
            # '-std=c++11' regardless of CMAKE_CXX_STANDARD value
            options.append(
                define(
                    "Trilinos_CXX11_FLAGS",
                    (
                        self.compiler.cxx14_flag
                        if spec.variants["cxxstd"].value == "14"
                        else self.compiler.cxx11_flag
                    ),
                )
            )

        # ################## Trilinos Packages #####################

        options.extend(
            [
                define_trilinos_enable("Adelus"),
                define_trilinos_enable("Amesos"),
                define_trilinos_enable("Amesos2"),
                define_trilinos_enable("Anasazi"),
                define_trilinos_enable("AztecOO", "aztec"),
                define_trilinos_enable("Belos"),
                define_trilinos_enable("Epetra"),
                define_trilinos_enable("EpetraExt"),
                define_trilinos_enable("FEI", False),
                define_trilinos_enable("Gtest"),
                define_trilinos_enable("Ifpack"),
                define_trilinos_enable("Ifpack2"),
                define_trilinos_enable("Intrepid"),
                define_trilinos_enable("Intrepid2"),
                define_trilinos_enable("Isorropia"),
                define_trilinos_enable("Kokkos"),
                define_trilinos_enable("MiniTensor"),
                define_trilinos_enable("Mesquite"),
                define_trilinos_enable("ML"),
                define_trilinos_enable("MueLu"),
                define_trilinos_enable("NOX"),
                define_trilinos_enable("Pamgen"),
                define_trilinos_enable("Panzer"),
                define_trilinos_enable("Pike", False),
                define_trilinos_enable("Piro"),
                define_trilinos_enable("Phalanx"),
                define_trilinos_enable("ROL"),
                define_trilinos_enable("Rythmos"),
                define_trilinos_enable("Sacado"),
                define_trilinos_enable("SCOREC"),
                define_trilinos_enable("Shards"),
                define_trilinos_enable("ShyLU"),
                define_trilinos_enable("STK"),
                define_trilinos_enable("Stokhos"),
                define_trilinos_enable("Stratimikos"),
                define_trilinos_enable("Teko"),
                define_trilinos_enable("Tempus"),
                define_trilinos_enable("Thyra"),
                define_trilinos_enable("Tpetra"),
                define_trilinos_enable("TrilinosCouplings"),
                define_trilinos_enable("Triutils", True),
                define_trilinos_enable("Zoltan"),
                define_trilinos_enable("Zoltan2"),
                define_from_variant("EpetraExt_BUILD_BTF", "epetraextbtf"),
                define_from_variant("EpetraExt_BUILD_EXPERIMENTAL", "epetraextexperimental"),
                define_from_variant(
                    "EpetraExt_BUILD_GRAPH_REORDERINGS", "epetraextgraphreorderings"
                ),
                define_from_variant("Amesos2_ENABLE_Basker", "basker"),
                define_from_variant("Amesos2_ENABLE_LAPACK", "amesos2"),
                define_from_variant("Amesos2_ENABLE_MUMPS", "mumps"),
            ]
        )

        if "+dtk" in spec:
            options.extend(
                [
                    define("Trilinos_EXTRA_REPOSITORIES", "DataTransferKit"),
                    define_trilinos_enable("DataTransferKit", True),
                ]
            )

        if "+exodus" in spec:
            options.extend(
                [
                    define_trilinos_enable("SEACAS", True),
                    define_trilinos_enable("SEACASExodus", True),
                    define_trilinos_enable("SEACASIoss", True),
                    define_trilinos_enable("SEACASEpu", True),
                    define_trilinos_enable("SEACASExodiff", True),
                    define_trilinos_enable("SEACASNemspread", True),
                    define_trilinos_enable("SEACASNemslice", True),
                ]
            )
        else:
            options.extend(
                [
                    define_trilinos_enable("SEACASExodus", False),
                    define_trilinos_enable("SEACASIoss", False),
                ]
            )

        if "+chaco" in spec:
            options.extend(
                [
                    define_trilinos_enable("SEACAS", True),
                    define_trilinos_enable("SEACASChaco", True),
                ]
            )
        else:
            # don't disable SEACAS, could be needed elsewhere
            options.extend(
                [
                    define_trilinos_enable("SEACASChaco", False),
                    define_trilinos_enable("SEACASNemslice", False),
                ]
            )

        if "@15: +python" in spec:
            binder = spec["binder"].prefix.bin.binder
            clang_include_dirs = spec["binder"].clang_include_dirs
            libclang_include_dir = spec["binder"].libclang_include_dir
            options.append(define("PyTrilinos2_BINDER_EXECUTABLE", binder))
            options.append(define("PyTrilinos2_BINDER_clang_include_dirs", clang_include_dirs))
            options.append(define("PyTrilinos2_BINDER_LibClang_include_dir", libclang_include_dir))
            options.append(define_from_variant("PyTrilinos2_ENABLE_TESTS", "test"))

        if "+stratimikos" in spec:
            # Explicitly enable Thyra (ThyraCore is required). If you don't do
            # this, then you get "NOT setting ${pkg}_ENABLE_Thyra=ON since
            # Thyra is NOT enabled at this point!" leading to eventual build
            # errors if using MueLu because `Xpetra_ENABLE_Thyra` is set to
            # off.

            # Add thyra adapters based on package enables
            options.extend(
                define_trilinos_enable("Thyra" + pkg + "Adapters", pkg.lower())
                for pkg in ["Epetra", "EpetraExt", "Tpetra"]
            )

        # ######################### TPLs #############################

        def define_tpl(trilinos_name, spack_name, have_dep):
            options.append(define("TPL_ENABLE_" + trilinos_name, have_dep))
            if not have_dep:
                return
            depspec = spec[spack_name]
            libs = depspec.libs
            try:
                options.extend(
                    [define(trilinos_name + "_INCLUDE_DIRS", depspec.headers.directories)]
                )
            except NoHeadersError:
                # Handle case were depspec does not have headers
                pass

            options.extend(
                [
                    define(trilinos_name + "_ROOT", depspec.prefix),
                    define(trilinos_name + "_LIBRARY_NAMES", libs.names),
                    define(trilinos_name + "_LIBRARY_DIRS", libs.directories),
                ]
            )

        # Enable these TPLs explicitly from variant options.
        # Format is (TPL name, variant name, Spack spec name)
        tpl_variant_map = [
            ("ADIOS2", "adios2", "adios2"),
            ("Boost", "boost", "boost"),
            ("CUDA", "cuda", "cuda"),
            ("HDF5", "hdf5", "hdf5"),
            ("HYPRE", "hypre", "hypre"),
            ("MUMPS", "mumps", "mumps"),
            ("AMD", "suite-sparse", "suite-sparse"),
            ("UMFPACK", "suite-sparse", "suite-sparse"),
            ("SuperLU", "superlu", "superlu"),
            ("SuperLUDist", "superlu-dist", "superlu-dist"),
            ("X11", "x11", "libx11"),
        ]
        if spec.satisfies("@13.0.2:"):
            tpl_variant_map.append(("STRUMPACK", "strumpack", "strumpack"))

        for tpl_name, var_name, spec_name in tpl_variant_map:
            define_tpl(tpl_name, spec_name, spec.variants[var_name].value)

        # Enable these TPLs based on whether they're in our spec; prefer to
        # require this way so that packages/features disable availability
        tpl_dep_map = [
            ("BLAS", "blas"),
            ("CGNS", "cgns"),
            ("LAPACK", "lapack"),
            ("Matio", "matio"),
            ("METIS", "metis"),
            ("Netcdf", "netcdf-c"),
            ("SCALAPACK", "scalapack"),
            ("Zlib", "zlib-api"),
        ]
        if spec.satisfies("@12.12.1:"):
            tpl_dep_map.append(("Pnetcdf", "parallel-netcdf"))
        if spec.satisfies("@13:") and not spec.satisfies("@develop"):
            tpl_dep_map.append(("HWLOC", "hwloc"))

        for tpl_name, dep_name in tpl_dep_map:
            define_tpl(tpl_name, dep_name, dep_name in spec)

        # External Kokkos
        if spec.satisfies("@14.4.0 +kokkos"):
            options.append(define_tpl_enable("Kokkos"))

        # MPI settings
        options.append(define_tpl_enable("MPI"))
        if "+mpi" in spec:
            # Force Trilinos to use the MPI wrappers instead of raw compilers
            # to propagate library link flags for linkers that require fully
            # resolved symbols in shared libs (such as macOS and some newer
            # Ubuntu)
            options.extend(
                [
                    define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
                    define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
                    define("MPI_BASE_DIR", str(pathlib.PurePosixPath(spec["mpi"].prefix))),
                ]
            )

        # ParMETIS dependencies have to be transitive explicitly
        have_parmetis = "parmetis" in spec
        options.append(define_tpl_enable("ParMETIS", have_parmetis))
        if have_parmetis:
            options.extend(
                [
                    define(
                        "ParMETIS_LIBRARY_DIRS",
                        [spec["parmetis"].prefix.lib, spec["metis"].prefix.lib],
                    ),
                    define("ParMETIS_LIBRARY_NAMES", ["parmetis", "metis"]),
                    define(
                        "TPL_ParMETIS_INCLUDE_DIRS",
                        spec["parmetis"].headers.directories + spec["metis"].headers.directories,
                    ),
                ]
            )

        if spec.satisfies("^superlu-dist@4.0:"):
            options.extend([define("HAVE_SUPERLUDIST_LUSTRUCTINIT_2ARG", True)])

        if spec.satisfies("^parallel-netcdf"):
            options.extend(
                [
                    define("TPL_Netcdf_Enables_Netcdf4", True),
                    define("TPL_Netcdf_PARALLEL", True),
                    define("PNetCDF_ROOT", spec["parallel-netcdf"].prefix),
                ]
            )

        options.append(define_tpl_enable("Cholmod", False))

        if spec.satisfies("platform=darwin"):
            # Don't let TriBITS define `libdl` as an absolute path to
            # the MacOSX{nn.n}.sdk since that breaks at every xcode update
            options.append(define_tpl_enable("DLlib", False))

        # ################# Explicit template instantiation #################

        complex_s = spec.variants["complex"].value
        float_s = spec.variants["float"].value

        options.extend(
            [define("Teuchos_ENABLE_COMPLEX", complex_s), define("Teuchos_ENABLE_FLOAT", float_s)]
        )

        if "+tpetra +explicit_template_instantiation" in spec:
            options.append(define_from_variant("Tpetra_INST_OPENMP", "openmp"))
            options.extend(
                [
                    define("Tpetra_INST_DOUBLE", True),
                    define("Tpetra_INST_COMPLEX_DOUBLE", complex_s),
                    define("Tpetra_INST_COMPLEX_FLOAT", float_s and complex_s),
                    define("Tpetra_INST_FLOAT", float_s),
                    define("Tpetra_INST_SERIAL", True),
                ]
            )

            gotype = spec.variants["gotype"].value
            if gotype == "all":
                # default in older Trilinos versions to enable multiple GOs
                options.extend(
                    [
                        define("Tpetra_INST_INT_INT", True),
                        define("Tpetra_INST_INT_LONG", True),
                        define("Tpetra_INST_INT_LONG_LONG", True),
                    ]
                )
            else:
                options.extend(
                    [
                        define("Tpetra_INST_INT_INT", gotype == "int"),
                        define("Tpetra_INST_INT_LONG", gotype == "long"),
                        define("Tpetra_INST_INT_LONG_LONG", gotype == "long_long"),
                    ]
                )

        # ################# Kokkos ######################

        if "+kokkos" in spec:
            arch = Kokkos.get_microarch(spec.target)
            if arch:
                options.append(define("Kokkos_ARCH_" + arch.upper(), True))

            define_kok_enable = _make_definer("Kokkos_ENABLE_")
            options.extend(
                [
                    define_kok_enable("CUDA"),
                    define_kok_enable("OPENMP" if spec.version >= Version("13") else "OpenMP"),
                ]
            )
            if "+cuda" in spec:
                use_uvm = "+uvm" in spec
                options.extend(
                    [
                        define_kok_enable("CUDA_UVM", use_uvm),
                        define_kok_enable("CUDA_LAMBDA", True),
                        define_kok_enable("CUDA_CONSTEXPR", "cuda_constexpr"),
                        define_kok_enable("CUDA_RELOCATABLE_DEVICE_CODE", "cuda_rdc"),
                    ]
                )
                arch_map = Kokkos.spack_cuda_arch_map
                options.extend(
                    define("Kokkos_ARCH_" + arch_map[arch].upper(), True)
                    for arch in spec.variants["cuda_arch"].value
                )

            if "+rocm" in spec:
                options.extend(
                    [
                        define_kok_enable("ROCM", False),
                        define_kok_enable("HIP", True),
                        define_kok_enable("HIP_RELOCATABLE_DEVICE_CODE", "rocm_rdc"),
                    ]
                )
                if "+tpetra" in spec:
                    options.append(define("Tpetra_INST_HIP", True))
                amdgpu_arch_map = Kokkos.amdgpu_arch_map
                for amd_target in spec.variants["amdgpu_target"].value:
                    try:
                        arch = amdgpu_arch_map[amd_target]
                    except KeyError:
                        pass
                    else:
                        options.append(define("Kokkos_ARCH_" + arch.upper(), True))

        # ################# System-specific ######################

        if sys.platform == "darwin" and macos_version() >= Version("10.12"):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append(define("CMAKE_MACOSX_RPATH", True))
        else:
            options.append(define("CMAKE_INSTALL_NAME_DIR", self.prefix.lib))

        return options

    @run_after("install")
    def filter_python(self):
        # When trilinos is built with Python, libpytrilinos is included
        # through cmake configure files. Namely, Trilinos_LIBRARIES in
        # TrilinosConfig.cmake contains pytrilinos. This leads to a
        # run-time error: Symbol not found: _PyBool_Type and prevents
        # Trilinos to be used in any C++ code, which links executable
        # against the libraries listed in Trilinos_LIBRARIES.  See
        # https://github.com/trilinos/Trilinos/issues/569 and
        # https://github.com/trilinos/Trilinos/issues/866
        # A workaround is to remove PyTrilinos from the COMPONENTS_LIST
        # and to remove -lpytrilonos from Makefile.export.Trilinos
        if self.spec.satisfies("@:13.0.1 +python"):
            filter_file(
                r"(SET\(COMPONENTS_LIST.*)(PyTrilinos;)(.*)",
                (r"\1\3"),
                "%s/cmake/Trilinos/TrilinosConfig.cmake" % self.prefix.lib,
            )
            filter_file(r"-lpytrilinos", "", "%s/Makefile.export.Trilinos" % self.prefix.include)

    def setup_run_environment(self, env):
        if "+exodus" in self.spec:
            env.prepend_path("PYTHONPATH", self.prefix.lib)

        if "+cuda" in self.spec:
            # currently Trilinos doesn't perform the memory fence so
            # it relies on blocking CUDA kernel launch.
            env.set("CUDA_LAUNCH_BLOCKING", "1")

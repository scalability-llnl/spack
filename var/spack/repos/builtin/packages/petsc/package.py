# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import llnl.util.tty as tty

from spack.package import *


class Petsc(Package, CudaPackage, ROCmPackage):
    """PETSc is a suite of data structures and routines for the scalable
    (parallel) solution of scientific applications modeled by partial
    differential equations.
    """

    homepage = "https://petsc.org"
    url = "https://web.cels.anl.gov/projects/petsc/download/release-snapshots/petsc-3.20.0.tar.gz"
    git = "https://gitlab.com/petsc/petsc.git"
    maintainers("balay", "barrysmith", "jedbrown")

    tags = ["e4s"]

    version("main", branch="main")
    version("3.22.0", sha256="2c03f7c0f7ad2649240d4989355cf7fb7f211b75156cd7d424e1d9dd7dfb290b")
    version("3.21.6", sha256="cb2dc00742a89cf8acf9ff8aae189e6864e8b90f4997f087be6e54ff39c30d74")
    version("3.21.5", sha256="4eb1ec04c1a8988bd524f71f8d7d980dc1853d5be8791c0f19f3c09eef71fdd2")
    version("3.21.4", sha256="a9ae076d4617c7d84ce2bed37194022319c19f19b3930edf148b2bc8ecf2248d")
    version("3.21.3", sha256="6d9ceb99d84d275250c614192dad45955d4a7610e12d8292a07dc49403556d26")
    version("3.21.2", sha256="a1ac62b6204bdf2f7f9b637abf45e6cff24d372d4d3d3702c50e157bdb56eb21")
    version("3.21.1", sha256="7ff8b692bceb7d7a8f51e2f45ccb20af00ba9395d7e1eee8816d46eb1c4c4b27")
    version("3.21.0", sha256="1e0c2f92514c72f80d4a4d0e6439a3aba0ceda7a0bcbc7ad9c44ce4cd8b14c28")
    version("3.20.6", sha256="20e6c260765f9593924bc5b1783bd152ec5c47246b47ce516cded7b505b34795")
    version("3.20.5", sha256="fb4e637758737af910b05f30a785245633916cd0a929b7b6447ad1028da4ea5a")
    version("3.20.4", sha256="b0d03a5595ee0a5696dd6683321e1dbfe9fea85238d3016a847b3d0bcdcfb3d9")
    version("3.20.3", sha256="75a94fb44df0512f51ad093fa784e56b61f51b7ead5956fbe49185c203f8c245")
    version("3.20.2", sha256="2a2d08b5f0e3d0198dae2c42ce1fd036f25c153ef2bb4a2d320ca141ac7cd30b")
    version("3.20.1", sha256="3d54f13000c9c8ceb13ca4f24f93d838319019d29e6de5244551a3ec22704f32")
    version("3.20.0", sha256="c152ccb12cb2353369d27a65470d4044a0c67e0b69814368249976f5bb232bd4")
    version("3.19.6", sha256="6045e379464e91bb2ef776f22a08a1bc1ff5796ffd6825f15270159cbb2464ae")
    version("3.19.5", sha256="511aa78cad36db2dfd298acf35e9f7afd2ecc1f089da5b0b5682507a31a5d6b2")
    version("3.19.4", sha256="7c941b71be52c3b764214e492df60109d12f97f7d854c97a44df0c4d958b3906")
    version("3.19.3", sha256="008239c016b869693ec8e81368a0b7638462e667d07f7d50ed5f9b75ccc58d17")
    version("3.19.2", sha256="114f363f779bb16839b25c0e70f8b0ae0d947d50e72f7c6cddcb11b001079b16")
    version("3.19.1", sha256="74db60c53c80b48d5c39e07bc39a883ecced88b9f24a5de17cf6f485a903e120")
    version("3.19.0", sha256="8ced753e4d2fb6565662b2b1fbba75a426cbf8438203f82717ce270f0591322c")
    version("3.18.6", sha256="8b53c8b6652459ba0bbe6361b5baf8c4d17c1d04b6654a76e3b6a9ab4a576680")
    version("3.18.5", sha256="df73ae13a4c5758325a9d69350cac423742657d8a8fc5782504b0e469ce46499")
    version("3.18.4", sha256="6173d30637261c5b740c0bea14747759200ca2012c7343139f9216bc296a6394")
    version("3.18.3", sha256="8aaa005479c8ec2eed2b9cbb067cfc1ac0900b0de2176439f0d4f21e09c2020b")
    version("3.18.2", sha256="4e055f92f3d5123d415f6f3ccf5ede9989f16d9e1f71cc7998ad244a3d3562f4")
    version("3.18.1", sha256="02f5979a22f5961bb775d527f8450db77bc6a8d2541f3b05fb586829b82e9bc8")
    version("3.18.0", sha256="9da802e703ad79fb7ef0007d17f68916573011073ee9712dcd1673537f6a5f68")
    version("3.17.5", sha256="a1193e6c50a1676c3972a1edf0a06eec9fac8ecc2f3771f2689a8997423e4c71")
    version("3.17.4", sha256="99c127486722a3ffd95a268b4ceb0976cbf217926c681a9631bd7246eab8cb2a")
    version("3.17.3", sha256="5c24ade5e4b32cc04935ba0db1dafe48d633bebaaa30a3033f1e58788d37875f")
    version("3.17.2", sha256="2313dd1ca41bf0ace68671ea6f8d4abf90011ed899f5e1e08658d3f18478359d")
    version("3.17.1", sha256="c504609d9f532327c20b6363d6a6c7647ebd3c98acfb382c28fcd3852300ddd1")
    version("3.17.0", sha256="96d5aca684e1ce1425891a620d278773c25611cb144165a93b17531238eaaf8a")
    version("3.16.6", sha256="bfc836b52f57686b583c16ab7fae0c318a7b28141ca01656ad673c8ca23037fa")
    version("3.16.5", sha256="7de8570eeb94062752d82a83208fc2bafc77b3f515023a4c14d8ff9440e66cac")
    version("3.16.4", sha256="229cce22bdcfedb1fe827d306ed1afca9737786cdc3f0562b74a1966c1243caf")
    version("3.16.3", sha256="eff44c7e7f12991dc7d2b627c477807a215ce16c2ce8a1c78aa8237ddacf6ca5")
    version("3.16.2", sha256="7ab257ae150d4837ac8d3872a1d206997962578785ec2427639ceac46d131bbc")
    version("3.16.1", sha256="909cf7bce7b6a0ddb2580a1ac9502aa01631ec4105c716594c1804f0ee1ea06a")
    version("3.16.0", sha256="5aaad7deea127a4790c8aa95c42fd9451ab10b5d6c68b226b92d4853002f438d")
    version("3.15.5", sha256="67dc31f1c1c941a0e45301ed4042628586e92e8c4e9b119695717ae782ef23a3")
    version("3.15.4", sha256="1e62fb0859a12891022765d1e24660cfcd704291c58667082d81a0618d6b0047")
    version("3.15.3", sha256="483028088020001e6f8d57b78a7fc880ed52d6693f57d627779c428f55cff73d")
    version("3.15.2", sha256="3b10c19c69fc42e01a38132668724a01f1da56f5c353105cd28f1120cc9041d8")
    version("3.15.1", sha256="c0ac6566e69d1d70b431e07e7598e9de95e84891c2452db1367c846b75109deb")
    version("3.15.0", sha256="ac46db6bfcaaec8cd28335231076815bd5438f401a4a05e33736b4f9ff12e59a")
    version("3.14.6", sha256="4de0c8820419fb15bc683b780127ff57067b62ca18749e864a87c6d7c93f1230")
    version("3.14.5", sha256="8b8ff5c4e10468f696803b354a502d690c7d25c19d694a7e10008a302fdbb048")
    version("3.14.4", sha256="b030969816e02c251a6d010c07a90b69ade44932f9ddfac3090ff5e95ab97d5c")
    version("3.14.3", sha256="63ed7e3440f2bbc732a6c44aa878364f88f5016ab375d9b36d742893a049053d")
    version("3.14.2", sha256="87a04fd05cac20a2ec47094b7d18b96e0651257d8c768ced2ef7db270ecfb9cb")
    version("3.14.1", sha256="0b4681165a9af96594c794b97ac6993452ec902726679f6b50bb450f89d230ed")
    version("3.14.0", sha256="a8f9caba03e0d57d8452c08505cf96be5f6949adaa266e819382162c03ddb9c5")
    version("3.13.6", sha256="67ca2cf3040d08fdc51d27f660ea3157732b24c2f47aae1b19d63f62a39842c2")
    version("3.13.5", sha256="10fc542dab961c8b17db35ad3a208cb184c237fc84e183817e38e6c7ab4b8732")
    version("3.13.4", sha256="8d470cba1ceb9638694550134a2f23aac85ed7249cb74992581210597d978b94")
    version("3.13.3", sha256="dc744895ee6b9c4491ff817bef0d3abd680c5e3c25e601be44240ce65ab4f337")
    version("3.13.2", sha256="6083422a7c5b8e89e5e4ccf64acade9bf8ab70245e25bca3a3da03caf74602f1")
    version("3.13.1", sha256="74a895e44e2ff1146838aaccb7613e7626d99e0eed64ca032c87c72d084efac3")
    version("3.13.0", sha256="f0ea543a54145c5d1387e25b121c3fd1b1ca834032c5a33f6f1d929e95bdf0e5")
    version("3.12.5", sha256="d676eb67e79314d6cca6422d7c477d2b192c830b89d5edc6b46934f7453bcfc0")
    version("3.12.4", sha256="56a941130da93bbacb3cfa74dcacea1e3cd8e36a0341f9ced09977b1457084c3")
    version("3.12.3", sha256="91f77d7b0f54056f085b9e27938922db3d9bb1734a2e2a6d26f43d3e6c0cf631")
    version("3.12.2", sha256="d874b2e198c4cb73551c2eca1d2c5d27da710be4d00517adb8f9eb3d6d0375e8")
    version("3.12.1", sha256="b72d895d0f4a79acb13ebc782b47b26d10d4e5706d399f533afcd5b3dba13737")
    version("3.12.0", sha256="ba9ecf69783c7ebf05bd1c91dd1d4b38bf09b7a2d5f9a774aa6bb46deff7cb14")
    version("3.11.4", sha256="319cb5a875a692a67fe5b1b90009ba8f182e21921ae645d38106544aff20c3c1")
    version("3.11.3", sha256="199ad9650a9f58603b49e7fff7cd003ceb03aa231e5d37d0bf0496c6348eca81")
    version("3.11.2", sha256="4d244dd7d1565d6534e776445fcf6977a6ee2a8bb2be4a36ac1e0fc1f9ad9cfa")
    version("3.11.1", sha256="cb627f99f7ce1540ebbbf338189f89a5f1ecf3ab3b5b0e357f9e46c209f1fb23")
    version("3.11.0", sha256="b3bed2a9263193c84138052a1b92d47299c3490dd24d1d0bf79fb884e71e678a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("mpi", default=True, description="Activates MPI support")
    variant("double", default=True, description="Switches between single and double precision")
    variant("complex", default=False, description="Build with complex numbers")
    variant("debug", default=False, description="Compile in debug mode")
    variant("sycl", default=False, description="Enable sycl build")

    variant("metis", default=True, description="Activates support for metis and parmetis")
    variant(
        "ptscotch", default=False, description="Activates support for PTScotch (only parallel)"
    )
    variant("hdf5", default=True, description="Activates support for HDF5 (only parallel)")
    variant("hypre", default=True, description="Activates support for Hypre (only parallel)")
    variant("hpddm", default=False, description="Activates support for HPDDM (only parallel)")
    variant("mmg", default=False, description="Activates support for MMG")
    variant("parmmg", default=False, description="Activates support for ParMMG (only parallel)")
    variant("tetgen", default=False, description="Activates support for Tetgen")
    variant("zoltan", default=False, description="Activates support for Zoltan")
    # Mumps is disabled by default, because it depends on Scalapack
    # which is not portable to all HPC systems
    variant("mumps", default=False, description="Activates support for MUMPS (only parallel)")
    variant(
        "superlu-dist",
        default=True,
        when="+fortran",
        description="Activates support for superlu-dist (only parallel)",
    )
    variant("strumpack", default=False, description="Activates support for Strumpack")
    variant(
        "scalapack", default=False, when="+fortran", description="Activates support for Scalapack"
    )
    variant(
        "trilinos", default=False, description="Activates support for Trilinos (only parallel)"
    )
    variant("mkl-pardiso", default=False, description="Activates support for MKL Pardiso")
    variant("int64", default=False, description="Compile with 64bit indices")
    variant(
        "clanguage",
        default="C",
        values=("C", "C++"),
        description="Specify C (recommended) or C++ to compile PETSc",
        multi=False,
    )
    variant("fftw", default=False, description="Activates support for FFTW (only parallel)")
    variant("suite-sparse", default=False, description="Activates support for SuiteSparse")
    variant("knl", default=False, description="Build for KNL")
    variant("X", default=False, description="Activate X support")
    variant(
        "batch", default=False, description="Enable when mpiexec is not available to run binaries"
    )
    variant("valgrind", default=False, description="Enable Valgrind Client Request mechanism")
    variant("jpeg", default=False, description="Activates support for JPEG")
    variant("libpng", default=False, description="Activates support for PNG")
    variant("giflib", default=False, description="Activates support for GIF")
    variant("mpfr", default=False, description="Activates support for MPFR")
    variant("moab", default=False, description="Acivates support for MOAB (only parallel)")
    variant("random123", default=False, description="Activates support for Random123")
    variant(
        "exodusii", default=False, description="Activates support for ExodusII (only parallel)"
    )
    variant("cgns", default=False, description="Activates support for CGNS (only parallel)")
    variant("memkind", default=False, description="Activates support for Memkind")
    variant(
        "memalign",
        default="none",
        description="Specify alignment of allocated arrays",
        values=("4", "8", "16", "32", "64", "none"),
        multi=False,
    )
    variant("p4est", default=False, description="Activates support for P4Est (only parallel)")
    variant("saws", default=False, description="Activates support for Saws")
    variant("libyaml", default=False, description="Activates support for YAML")
    variant("openmp", default=False, description="Activates support for openmp")
    variant("hwloc", default=False, description="Activates support for hwloc")
    variant("kokkos", default=False, description="Activates support for kokkos and kokkos-kernels")
    variant("fortran", default=True, description="Activates fortran support")

    with when("+rocm"):
        # https://github.com/spack/spack/issues/37416
        conflicts("^rocprim@5.3.0:5.3.2")
        # hipsparse@5.6.0 broke hipsparseSpSV_solve() API, reverted in 5.6.1.
        patch(
            "https://gitlab.com/petsc/petsc/-/commit/ef7140cce45367033b48bbd2624dfd2b6aa4b997.diff",
            when="@3.20.0",
            sha256="ba327f8b2a0fa45209dfb7a4278f3e9a323965b5a668be204c1c77c17a963a7f",
        )
        patch(
            "https://gitlab.com/petsc/petsc/-/commit/20d5ecbf88175ced320006c488dcefa2efb1e67f.diff",
            when="@3.21 ^hip@6:",
            sha256="2904ea20c71e2f21b8475513c3e5de7465e328e2485ae706b003aa79314e3e7c",
        )
        patch(
            "https://gitlab.com/petsc/petsc/-/commit/bdb83d9f3e3c55b3bd4c8732bfe2066c23f10f61.diff",
            when="@3.21 ^hip@6:",
            sha256="89cf2c9a01d4a3233c889dd98496a29bf43db1bc69195892f9e5405c537b87e3",
        )
        patch("hip-5.6.0-for-3.18.diff", when="@3.18:3.19 ^hipsparse@5.6.0")
        patch("hip-5.7-plus-for-3.18.diff", when="@3.18:3.19 ^hipsparse@5.7:")
        patch(
            "0001-Handle-the-hipsparse-api-changes-for-rocm-6.0.patch",
            when="@3.20.2:3.20.4 ^hipsparse@6.0",
        )

    # 3.8.0 has a build issue with MKL - so list this conflict explicitly
    conflicts("^intel-mkl", when="@3.8.0")

    # These require +mpi
    mpi_msg = "Requires +mpi"
    conflicts("+cgns", when="~mpi", msg=mpi_msg)
    conflicts("+exodusii", when="~mpi", msg=mpi_msg)
    conflicts("+fftw", when="~mpi", msg=mpi_msg)
    conflicts("+hdf5", when="~mpi", msg=mpi_msg)
    conflicts("+hypre", when="~mpi", msg=mpi_msg)
    conflicts("+hpddm", when="~mpi", msg=mpi_msg)
    conflicts("+parmmg", when="~mpi", msg=mpi_msg)
    conflicts("+moab", when="~mpi", msg=mpi_msg)
    conflicts("+mumps", when="~mpi", msg=mpi_msg)
    conflicts("+p4est", when="~mpi", msg=mpi_msg)
    conflicts("+ptscotch", when="~mpi", msg=mpi_msg)
    conflicts("+superlu-dist", when="~mpi", msg=mpi_msg)
    conflicts("+trilinos", when="~mpi", msg=mpi_msg)
    conflicts("+kokkos", when="~mpi", msg=mpi_msg)
    conflicts("^openmpi~cuda", when="+cuda")  # +cuda requires CUDA enabled OpenMPI

    # older versions of petsc did not support mumps when +int64
    conflicts("+mumps", when="@:3.12+int64")

    filter_compiler_wrappers("petscvariables", relative_root="lib/petsc/conf")

    @run_before("configure")
    def check_fortran_compiler(self):
        # Raise error if +fortran and there isn't a fortran compiler!
        if "+fortran" in self.spec and self.compiler.fc is None:
            raise InstallError("+fortran requires a fortran compiler!")

    # temporary workaround Clang 8.1.0 with XCode 8.3 on macOS, see
    # https://bitbucket.org/petsc/petsc/commits/4f290403fdd060d09d5cb07345cbfd52670e3cbc
    # the patch is an adaptation of the original commit to 3.7.5
    patch("macos-clang-8.1.0.diff", when="@3.7.5%apple-clang@8.1.0:")
    patch("pkg-config-3.7.6-3.8.4.diff", when="@3.7.6:3.8.4")
    patch("xcode_stub_out_of_sync.patch", when="@:3.10.4")
    patch("xlf_fix-dup-petscfecreate.patch", when="@3.11.0")
    patch("disable-DEPRECATED_ENUM.diff", when="@3.14.1 +cuda")
    patch("revert-3.18.0-ver-format-for-dealii.patch", when="@3.18.0")

    depends_on("diffutils", type="build")
    # not listed as a "build" dependency - so that slepc build gets the same dependency
    depends_on("gmake")

    # Virtual dependencies
    # Git repository needs sowing to build Fortran interface
    depends_on("sowing@master", when="@main")

    # PETSc, hypre, superlu_dist when built with int64 use 32 bit integers
    # with BLAS/LAPACK
    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("cuda", when="+cuda")
    # Fixed in https://gitlab.com/petsc/petsc/-/merge_requests/7354
    conflicts(
        "^cuda@12.4:", when="@:3.20.5 +cuda", msg="Deprecation in CCCL 2.3 causes build failure."
    )
    depends_on("hip", when="+rocm")

    with when("+rocm"):
        depends_on("rocm-core")
        depends_on("hipblas")
        depends_on("hipsparse")
        depends_on("hipsolver")
        depends_on("rocsparse")
        depends_on("rocsolver")
        depends_on("rocblas")
        depends_on("rocrand")
        depends_on("rocthrust")
        depends_on("rocprim")

    with default_args(type="build"):
        depends_on("python@2.6:2.8,3.4:")
        depends_on("python@3.4:", when="@3.18:")
        depends_on("python@:3.8", when="@:3.13")
        depends_on("python@:3.12", when="@:3.21")  # import xdrlib

    # Other dependencies
    depends_on("metis@5:~int64+real64", when="@:3.7+metis~int64+double")
    depends_on("metis@5:~int64", when="@:3.7+metis~int64~double")
    depends_on("metis@5:+int64+real64", when="@:3.7+metis+int64+double")
    depends_on("metis@5:+int64", when="@:3.7+metis+int64~double")
    # petsc-3.8+ uses default (float) metis with any (petsc) precision
    depends_on("metis@5:~int64", when="@3.8:+metis~int64")
    depends_on("metis@5:+int64", when="@3.8:+metis+int64")

    # PTScotch: Currently disable Parmetis wrapper, this means
    # nested disection won't be available thought PTScotch
    depends_on("scotch+esmumps~metis+mpi", when="+ptscotch")
    depends_on("scotch+int64", when="+ptscotch+int64")

    depends_on("hdf5@:1.10+mpi", when="@:3.12+hdf5+mpi")
    depends_on("hdf5+mpi", when="@3.13:+hdf5+mpi")
    depends_on("hdf5+mpi", when="+exodusii+mpi")
    depends_on("hdf5+mpi", when="+cgns+mpi")
    depends_on("zlib-api", when="+hdf5")
    depends_on("zlib-api", when="+libpng")
    depends_on("zlib-api", when="+p4est")
    depends_on("parmetis+int64", when="+metis+mpi+int64")
    depends_on("parmetis~int64", when="+metis+mpi~int64")
    depends_on("valgrind", when="+valgrind")
    depends_on("mmg", when="+mmg")
    depends_on("mmg", when="+parmmg")
    depends_on("parmmg", when="+parmmg")
    depends_on("tetgen+pic", when="+tetgen")
    depends_on("zoltan", when="+zoltan")

    depends_on("hypre+fortran", when="+hypre+fortran")
    depends_on("hypre~fortran", when="+hypre~fortran")
    depends_on("hypre+complex", when="+hypre+complex")
    depends_on("hypre~complex", when="+hypre~complex")
    depends_on("hypre+int64", when="+hypre+int64")
    depends_on("hypre~int64", when="+hypre~int64")
    depends_on("hypre+mpi~internal-superlu", when="+hypre")
    depends_on("hypre@2.14:2.18.2", when="@3.11:3.13+hypre")
    depends_on("hypre@2.14:2.22.0", when="@3.14:3.15+hypre")
    depends_on("hypre@2.14:2.28.0", when="@3.16:3.19+hypre")
    depends_on("hypre@2.14:", when="@3.20+hypre")
    depends_on("hypre@develop", when="@main+hypre")

    depends_on("superlu-dist@:4.3~int64", when="@3.4.4:3.6.4+superlu-dist+mpi~int64")
    depends_on("superlu-dist@:4.3+int64", when="@3.4.4:3.6.4+superlu-dist+mpi+int64")
    depends_on("superlu-dist@5.0.0:5.1.3~int64", when="@3.7.0:3.7+superlu-dist+mpi~int64")
    depends_on("superlu-dist@5.0.0:5.1.3+int64", when="@3.7.0:3.7+superlu-dist+mpi+int64")
    depends_on("superlu-dist@5.2.0:5.2~int64", when="@3.8:3.9+superlu-dist+mpi~int64")
    depends_on("superlu-dist@5.2.0:5.2+int64", when="@3.8:3.9+superlu-dist+mpi+int64")
    depends_on("superlu-dist@5.4.0:5.4~int64", when="@3.10:3.10.2+superlu-dist+mpi~int64")
    depends_on("superlu-dist@5.4.0:5.4+int64", when="@3.10:3.10.2+superlu-dist+mpi+int64")
    depends_on("superlu-dist@6.1.0:6.1~int64", when="@3.10.3:3.12+superlu-dist+mpi~int64")
    depends_on("superlu-dist@6.1.0:6.1+int64", when="@3.10.3:3.12+superlu-dist+mpi+int64")
    depends_on("superlu-dist@6.1:~int64", when="@3.13.0:+superlu-dist+mpi~int64")
    depends_on("superlu-dist@6.1:+int64", when="@3.13.0:+superlu-dist+mpi+int64")
    depends_on("superlu-dist@develop~int64", when="@main+superlu-dist+mpi~int64")
    depends_on("superlu-dist@develop+int64", when="@main+superlu-dist+mpi+int64")
    depends_on("strumpack", when="+strumpack")
    depends_on("scalapack", when="+strumpack")
    depends_on("metis", when="+strumpack")
    depends_on("scalapack", when="+scalapack")
    depends_on("mumps+mpi~int64~metis~parmetis~openmp", when="+mumps~metis~openmp")
    depends_on("mumps+mpi~int64+metis+parmetis~openmp", when="+mumps+metis~openmp")
    depends_on("mumps+mpi~int64~metis~parmetis+openmp", when="+mumps~metis+openmp")
    depends_on("mumps+mpi~int64+metis+parmetis+openmp", when="+mumps+metis+openmp")
    depends_on("scalapack", when="+mumps")
    depends_on("trilinos@12.6.2:+mpi", when="@3.7.0:+trilinos+mpi")
    depends_on("trilinos@develop+mpi", when="@main+trilinos+mpi")
    depends_on("mkl", when="+mkl-pardiso")
    depends_on("fftw+mpi", when="+fftw+mpi")
    depends_on("suite-sparse", when="+suite-sparse")
    depends_on("libx11", when="+X")
    depends_on("mpfr", when="+mpfr")
    depends_on("gmp", when="+mpfr")
    depends_on("jpeg", when="+jpeg")
    depends_on("libpng", when="+libpng")
    depends_on("giflib", when="+giflib")
    depends_on("exodusii+mpi", when="+exodusii+mpi")
    depends_on("netcdf-c+mpi", when="+exodusii+mpi")
    depends_on("parallel-netcdf", when="+exodusii+mpi")
    depends_on("random123", when="+random123")
    depends_on("moab+mpi", when="+moab+mpi")
    depends_on("cgns+mpi", when="+cgns+mpi")
    depends_on("memkind", when="+memkind")
    depends_on("p4est+mpi", when="+p4est+mpi")
    depends_on("saws", when="+saws")
    depends_on("libyaml", when="+libyaml")
    depends_on("hwloc", when="+hwloc")
    depends_on("kokkos", when="+kokkos")
    depends_on("kokkos-kernels", when="+kokkos")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "kokkos+cuda+cuda_lambda cuda_arch=%s" % cuda_arch,
            when="+kokkos +cuda cuda_arch=%s" % cuda_arch,
        )
        depends_on(
            "kokkos-kernels+cuda cuda_arch=%s" % cuda_arch,
            when="+kokkos +cuda cuda_arch=%s" % cuda_arch,
        )
    for rocm_arch in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos+rocm amdgpu_target=%s" % rocm_arch,
            when="+kokkos +rocm amdgpu_target=%s" % rocm_arch,
        )

    conflicts("~kokkos", when="+sycl", msg="+sycl requires +kokkos")
    depends_on("kokkos+sycl", when="+sycl +kokkos")

    phases = ["configure", "build", "install"]

    # Using the following tarballs
    # * petsc-3.12 (and older) - includes docs
    # * petsc-lite-3.13, petsc-lite-3.14 (without docs)
    # * petsc-3.15 and newer (without docs)
    def url_for_version(self, version):
        if self.spec.satisfies("@3.13.0:3.14.6"):
            return "http://web.cels.anl.gov/projects/petsc/download/release-snapshots/petsc-lite-{0}.tar.gz".format(
                version
            )
        else:
            return "http://web.cels.anl.gov/projects/petsc/download/release-snapshots/petsc-{0}.tar.gz".format(
                version
            )

    def mpi_dependent_options(self):
        if "~mpi" in self.spec:
            compiler_opts = [
                "--with-cc=%s" % os.environ["CC"],
                "--with-cxx=%s" % (os.environ["CXX"] if self.compiler.cxx is not None else "0"),
                "--with-mpi=0",
            ]
            if "+fortran" in self.spec:
                compiler_opts.append("--with-fc=%s" % os.environ["FC"])
            else:
                compiler_opts.append("--with-fc=0")
        else:
            compiler_opts = [
                "--with-cc=%s" % self.spec["mpi"].mpicc,
                "--with-cxx=%s" % self.spec["mpi"].mpicxx,
            ]
            if "+fortran" in self.spec:
                compiler_opts.append("--with-fc=%s" % self.spec["mpi"].mpifc)
            else:
                compiler_opts.append("--with-fc=0")
            if self.spec.satisfies("%intel"):
                # mpiifort needs some help to automatically link
                # all necessary run-time libraries
                compiler_opts.append("--FC_LINKER_FLAGS=-lintlc")
        return compiler_opts

    def configure_options(self):
        spec = self.spec
        options = [
            "--with-ssl=0",
            "--download-c2html=0",
            "--download-sowing=0",
            "--download-hwloc=0",
            "--with-make-exec=%s" % make,
        ]
        # If 'cflags', 'fflags', and/or 'cxxflags' are not set, let the PETSc
        # configuration script choose defaults.
        if spec.compiler_flags["cflags"]:
            options += ["CFLAGS=%s" % " ".join(spec.compiler_flags["cflags"])]
            if "+debug" not in spec:
                options += ["COPTFLAGS="]
        if spec.compiler_flags["fflags"]:
            options += ["FFLAGS=%s" % " ".join(spec.compiler_flags["fflags"])]
            if "+debug" not in spec:
                options += ["FOPTFLAGS="]
        if spec.compiler_flags["cxxflags"]:
            options += ["CXXFLAGS=%s" % " ".join(spec.compiler_flags["cxxflags"])]
            if "+debug" not in spec:
                options += ["CXXOPTFLAGS="]
        options.extend(self.mpi_dependent_options())
        options.extend(
            [
                "--with-precision=%s" % ("double" if "+double" in spec else "single"),
                "--with-scalar-type=%s" % ("complex" if "+complex" in spec else "real"),
                "--with-shared-libraries=%s" % ("1" if "+shared" in spec else "0"),
                "--with-debugging=%s" % ("1" if "+debug" in spec else "0"),
                "--with-openmp=%s" % ("1" if "+openmp" in spec else "0"),
                "--with-64-bit-indices=%s" % ("1" if "+int64" in spec else "0"),
            ]
        )

        # Make sure we use exactly the same Blas/Lapack libraries
        # across the DAG. To that end list them explicitly
        lapack_blas = spec["lapack"].libs + spec["blas"].libs
        options.extend(["--with-blas-lapack-lib=%s" % lapack_blas.joined()])

        if "+batch" in spec:
            options.append("--with-batch=1")
        if "+knl" in spec:
            options.append("--with-avx-512-kernels")
            options.append("--with-memalign=64")
        elif self.spec.variants["memalign"].value != "none":
            alignement = self.spec.variants["memalign"].value
            options.append(f"--with-memalign={alignement}")

        if "+X" in spec:
            options.append("--with-x=1")
        else:
            options.append("--with-x=0")

        if "+sycl" in spec:
            sycl_compatible_compilers = ["icpx"]
            if not (os.path.basename(self.compiler.cxx) in sycl_compatible_compilers):
                raise InstallError("PETSc's SYCL GPU Backend requires oneAPI CXX (icpx) compiler.")
            options.append("--with-sycl=1")
            options.append("--with-syclc=" + self.compiler.cxx)
            options.append("SYCLPPFLAGS=-Wno-tautological-constant-compare")
        else:
            options.append("--with-sycl=0")

        if "trilinos" in spec:
            if spec.satisfies("^trilinos+boost"):
                options.append("--with-boost=1")

        if spec.satisfies("clanguage=C++"):
            options.append("--with-clanguage=C++")
        else:
            options.append("--with-clanguage=C")

        # to be used in the list of libraries below
        if "+fortran" in spec:
            hdf5libs = ":hl,fortran"
        else:
            hdf5libs = ":hl"

        # tuple format (spacklibname, petsclibname, useinc, uselib)
        # default: 'gmp', => ('gmp', 'gmp', True, True)
        # any other combination needs a full tuple
        # if not (useinc || uselib): usedir - i.e (False, False)
        direct_dependencies = []
        for dep in spec.dependencies():
            direct_dependencies.append(dep.name)
            direct_dependencies.extend(set(vspec.name for vspec in dep.package.virtuals_provided))
        for library in (
            ("cuda", "cuda", False, False),
            ("hip", "hip", True, False),
            "metis",
            "hypre",
            "parmetis",
            ("kokkos", "kokkos", False, False),
            ("kokkos-kernels", "kokkos-kernels", False, False),
            ("superlu-dist", "superlu_dist", True, True),
            ("scotch", "ptscotch", True, True),
            (
                "suite-sparse:umfpack,klu,cholmod,btf,ccolamd,colamd,camd,amd, \
                suitesparseconfig,spqr",
                "suitesparse",
                True,
                True,
            ),
            ("hdf5" + hdf5libs, "hdf5", True, True),
            ("zlib-api", "zlib", True, True),
            "mumps",
            ("trilinos", "trilinos", False, False),
            ("fftw:mpi", "fftw", True, True),
            ("valgrind", "valgrind", False, False),
            "gmp",
            "libpng",
            ("giflib", "giflib", False, False),
            "mpfr",
            ("netcdf-c", "netcdf", True, True),
            ("parallel-netcdf", "pnetcdf", True, True),
            ("moab", "moab", False, False),
            ("random123", "random123", False, False),
            "exodusii",
            "cgns",
            "memkind",
            "p4est",
            ("saws", "saws", False, False),
            ("libyaml", "yaml", True, True),
            "hwloc",
            ("jpeg", "libjpeg", True, True),
            ("scalapack", "scalapack", False, True),
            "strumpack",
            "mmg",
            "parmmg",
            ("tetgen", "tetgen", False, False),
            "zoltan",
        ):
            # Cannot check `library in spec` because of transitive deps
            # Cannot check variants because parmetis keys on +metis
            if isinstance(library, tuple):
                spacklibname, petsclibname, useinc, uselib = library
            else:
                spacklibname = library
                petsclibname = library
                useinc = True
                uselib = True

            library_requested = spacklibname.split(":")[0] in direct_dependencies
            options.append(
                "--with-{library}={value}".format(
                    library=petsclibname, value=("1" if library_requested else "0")
                )
            )
            if library_requested:
                if useinc or uselib:
                    if useinc:
                        options.append(
                            "--with-{library}-include={value}".format(
                                library=petsclibname, value=spec[spacklibname].prefix.include
                            )
                        )
                    if uselib:
                        options.append(
                            "--with-{library}-lib={value}".format(
                                library=petsclibname, value=spec[spacklibname].libs.joined()
                            )
                        )
                else:
                    options.append(
                        "--with-{library}-dir={path}".format(
                            library=petsclibname, path=spec[spacklibname].prefix
                        )
                    )

        if "+cuda" in spec:
            if not spec.satisfies("cuda_arch=none"):
                cuda_arch = spec.variants["cuda_arch"].value
                if spec.satisfies("@3.14:"):
                    options.append("--with-cuda-gencodearch={0}".format(cuda_arch[0]))
                else:
                    options.append(
                        "CUDAFLAGS=-gencode arch=compute_{0},code=sm_{0}".format(cuda_arch[0])
                    )
        if "+rocm" in spec:
            if not spec.satisfies("amdgpu_target=none"):
                hip_arch = spec.variants["amdgpu_target"].value
                options.append("--with-hip-arch={0}".format(hip_arch[0]))
            hip_pkgs = ["hipsparse", "hipblas", "hipsolver", "rocsparse", "rocsolver", "rocblas"]
            hip_ipkgs = hip_pkgs + ["rocthrust", "rocprim", "rocm-core"]
            hip_lpkgs = hip_pkgs
            if spec.satisfies("^rocrand@5.1:"):
                hip_ipkgs.extend(["rocrand"])
            else:
                hip_lpkgs.extend(["rocrand"])
            hip_inc = ""
            hip_lib = ""
            for pkg in hip_ipkgs:
                hip_inc += spec[pkg].headers.include_flags + " "
            for pkg in hip_lpkgs:
                hip_lib += spec[pkg].libs.joined() + " "
            options.append("HIPPPFLAGS=%s" % hip_inc)
            options.append("--with-hip-lib=%s -L%s -lamdhip64" % (hip_lib, spec["hip"].prefix.lib))

        if "superlu-dist" in spec:
            if spec.satisfies("@3.10.3:3.15"):
                options.append("--with-cxx-dialect=C++11")
            if spec["superlu-dist"].satisfies("+rocm"):
                # Suppress HIP header warning message, otherwise the PETSc
                # configuration fails:
                options.append("CXXPPFLAGS=-DROCM_NO_WRAPPER_HEADER_WARNING")

        if "+mkl-pardiso" in spec:
            options.append("--with-mkl_pardiso-dir=%s" % spec["mkl"].prefix)

        # For the moment, HPDDM does not work as a dependency
        # using download instead
        if "+hpddm" in spec:
            options.append("--download-hpddm")

        return options

    def revert_kokkos_nvcc_wrapper(self):
        # revert changes by kokkos-nvcc-wrapper
        if self.spec.satisfies("^kokkos+cuda+wrapper"):
            env["MPICH_CXX"] = env["CXX"]
            env["OMPI_CXX"] = env["CXX"]
            env["MPICXX_CXX"] = env["CXX"]

    def configure(self, spec, prefix):
        self.revert_kokkos_nvcc_wrapper()
        python("configure", "--prefix=%s" % prefix, *self.configure_options())

    def build(self, spec, prefix):
        self.revert_kokkos_nvcc_wrapper()
        if spec.satisfies("@:3.18.5"):
            make("OMAKE_PRINTDIR=%s" % make, "V=1")
        else:
            make("V=1")

    def install(self, spec, prefix):
        self.revert_kokkos_nvcc_wrapper()
        make("install", parallel=False)

        if self.run_tests:
            make('check PETSC_ARCH="" PETSC_DIR={0}'.format(prefix), parallel=False)

    def setup_build_environment(self, env):
        # configure fails if these env vars are set outside of Spack
        env.unset("PETSC_DIR")
        env.unset("PETSC_ARCH")

    def setup_run_environment(self, env):
        # Set PETSC_DIR in the module file
        env.set("PETSC_DIR", self.prefix)
        env.unset("PETSC_ARCH")

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Set up PETSC_DIR for everyone using PETSc package
        env.set("PETSC_DIR", self.prefix)
        env.unset("PETSC_ARCH")

    @property
    def archive_files(self):
        return [
            join_path(self.stage.source_path, "configure.log"),
            join_path(self.stage.source_path, "make.log"),
        ]

    @property
    def headers(self):
        return (
            find_headers("petsc", self.prefix.include, recursive=False) or None
        )  # return None to indicate failure

    # For the 'libs' property - use the default handler.

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        if not self.spec.satisfies("@3.13:"):
            tty.warn("Stand-alone tests only available for v3.13:")
            return

        cache_extra_test_sources(
            self,
            [join_path("src", "ksp", "ksp", "tutorials"), join_path("src", "snes", "tutorials")],
        )

    def get_runner(self):
        """Set key environment variables and return runner and options."""
        spec = self.spec
        env["PETSC_DIR"] = self.prefix
        env["PETSC_ARCH"] = ""
        if "+mpi" in spec:
            runexe = which(spec["mpi"].prefix.bin.mpiexec)
            runopt = ["-n", "4"]
        else:
            runexe = which(join_path(self.prefix.lib.petsc.bin, "petsc-mpiexec.uni"))
            runopt = ["-n", "1"]
        return runexe, runopt

    def test_ex50(self):
        """build and run ex50 to solve Poisson equation in 2D"""
        # solve Poisson equation in 2D to make sure nothing is broken:
        make = which("make")
        runexe, runopts = self.get_runner()

        w_dir = self.test_suite.current_test_cache_dir.src.ksp.ksp.tutorials
        with working_dir(w_dir):
            baseopts = ["ex50", "-da_grid_x", "4", "-da_grid_y", "4"]
            testdict = {
                None: [],
                "+superlu-dist": ["-pc_type", "lu", "-pc_factor_mat_solver_type", "superlu_dist"],
                "+mumps": ["-pc_type", "lu", "-pc_factor_mat_solver_type", "mumps"],
                "+hypre": ["-pc_type", "hypre", "-pc_hypre_type", "boomeramg"],
                "+mkl-pardiso": ["-pc_type", "lu", "-pc_factor_mat_solver_type", "mkl_pardiso"],
            }
            make("ex50", parallel=False)
            for feature, featureopts in testdict.items():
                if not feature or feature in self.spec:
                    name = f"_{feature[1:]}" if feature else ""
                    options = runopts + baseopts + featureopts
                    with test_part(self, f"test_ex50{name}", purpose=f"run {options}"):
                        runexe(*options)

    def test_ex7(self):
        """build and run ex7"""
        if "+cuda" not in self.spec:
            raise SkipTest("Package must be built with +cuda")

        make = which("make")
        runexe, runopts = self.get_runner()

        w_dir = self.test_suite.current_test_cache_dir.src.ksp.ksp.tutorials
        with working_dir(w_dir):
            make("ex7", parallel=False)
            exeopts = [
                "ex7",
                "-mat_type",
                "aijcusparse",
                "-sub_pc_factor_mat_solver_type",
                "cusparse",
                "-sub_ksp_type",
                "preonly",
                "-sub_pc_type",
                "ilu",
                "-use_gpu_aware_mpi",
                "0",
            ]
            options = runopts + exeopts
            runexe(*options)

    def test_ex3k(self):
        """build and run ex3k"""
        if "+kokkos" not in self.spec:
            raise SkipTest("Package must be built with +kokkos")

        make = which("make")
        runexe, runopts = self.get_runner()

        w_dir = self.test_suite.current_test_cache_dir.src.snes.tutorials
        with working_dir(w_dir):
            make("ex3k", parallel=False)
            exeopts = [
                "ex3k",
                "-view_initial",
                "-dm_vec_type",
                "kokkos",
                "-dm_mat_type",
                "aijkokkos",
                "-use_gpu_aware_mpi",
                "0",
                "-snes_monitor",
            ]
            options = runopts + exeopts
            runexe(*options)

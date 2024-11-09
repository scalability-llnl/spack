# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack.package import *


class Qmcpack(CMakePackage, CudaPackage):
    """QMCPACK, is a modern high-performance open-source Quantum Monte
    Carlo (QMC) simulation code."""

    # Package information
    homepage = "https://www.qmcpack.org/"
    git = "https://github.com/QMCPACK/qmcpack.git"
    maintainers("ye-luo")
    tags = ["ecp", "ecp-apps"]

    license("CC0-1.0")

    # This download method is untrusted, and is not recommended by the
    # Spack manual. However, it is easier to maintain because github hashes
    # can occasionally change.
    # NOTE: 12/19/2017 QMCPACK 3.0.0 does not build properly with Spack.
    version("develop")
    version("3.17.1", tag="v3.17.1", commit="9d0d968139fc33f71dbf9159f526dd7b47f10a3b")
    version("3.17.0", tag="v3.17.0", commit="9049a90626d1fe3c431f55c56a7197f8a13d5fc6")
    version("3.16.0", tag="v3.16.0", commit="5b7544c40be105b0aafa1602601ccb0cf23ea547")
    version("3.15.0", tag="v3.15.0", commit="690350ae148a1345b57e610f240d800384514d69")
    version("3.14.0", tag="v3.14.0", commit="dbe4cebbd5f88ce42bf2deab5e571e64398e07ed")
    version("3.13.0", tag="v3.13.0", commit="5f4ba013eceaf437530d5792dac5c08760d51c96")
    version("3.12.0", tag="v3.12.0", commit="262d1915135aaf5786d9481765f79f48d3309533")
    version("3.11.0", tag="v3.11.0", commit="129b7d88497b27de9efd4f2cf56d83b97541f0f0")
    version("3.10.0", tag="v3.10.0", commit="f775d65b313b16b4ab22ecad40a968c0a6675ddc")
    version("3.9.2", tag="v3.9.2", commit="8064ebfec9a8dd88748e8864013168c9aa7e05dd")
    version("3.9.1", tag="v3.9.1", commit="e53d0b905ca2870c8c58b14437165addc6a6296f")
    version("3.9.0", tag="v3.9.0", commit="a5c74d4327e4ba84c097fd904ce2b696bf2735ae")
    version("3.8.0", tag="v3.8.0", commit="6abbff0b825dae52097f7965bdb549f84aed75cb")
    version("3.7.0", tag="v3.7.0", commit="bc47a435682751c26c2695a005684d95f700bebb")
    version("3.6.0", tag="v3.6.0", commit="91aca74ecb4e64bdccc7e05b28eda4653f8c07ff")
    version("3.5.0", tag="v3.5.0", commit="1009b07ad6fa873d71a0755747e6a7f610eb169b")
    version("3.4.0", tag="v3.4.0", commit="2d4b3d01224f7a4868da71d715e831341b2e7e5e")
    version("3.3.0", tag="v3.3.0", commit="ff1599015f0695a75436f2942f257d3a29b8b752")
    version("3.2.0", tag="v3.2.0", commit="d531f6b35fbab9ab2b80e9222f694b66e08bdd9d")
    version("3.1.1", tag="v3.1.1", commit="07611637f823187ac5133d6e2249cdb86b92b04d")
    version("3.1.0", tag="v3.1.0", commit="146d920cf33590eac6a7a976f88871c1fe6418a6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # These defaults match those in the QMCPACK manual
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )
    variant("mpi", default=True, description="Build with MPI support")
    variant("phdf5", default=False, description="Build with parallel collective I/O")
    variant(
        "complex", default=False, description="Build the complex (general twist/k-point) version"
    )
    variant(
        "mixed",
        default=False,
        description="Build the mixed precision (mixture of single and "
        "double precision) version",
    )
    variant(
        "soa",
        default=True,
        description="Build with Structure-of-Array (SoA) instead of "
        "Array-of-Structure code (AoS). This is a legacy "
        "option and the AoS code is not available after  "
        "v3.10.0. Only affected performance, not results.",
    )
    variant("timers", default=True, description="Build with support for timers")
    variant("da", default=False, description="Install with support for basic data analysis tools")
    variant("gui", default=False, description="Install with Matplotlib (long installation time)")
    variant(
        "afqmc",
        default=False,
        description="Install with AFQMC support. NOTE that if used in "
        "combination with CUDA, only AFQMC will have CUDA.",
    )
    variant("ppconvert", default=False, description="Install with pseudopotential converter.")

    # Notes about CUDA-centric peculiarities:
    #
    # cuda variant implies mixed precision variant by default, but there is
    # no way to express this in variant syntax, need something like
    # variant('+mixed', default=True, when='+cuda', description="...")
    #
    # cuda+afqmc variant will not build the legacy CUDA code in real-space
    # QMCPACK. This is due to a conflict in the build system. This is not
    # worth fixing since the legacy CUDA code, will be superseded
    # by the OpenMP 4.5 code.

    # high-level variant conflicts
    conflicts("~soa", when="@3.10.0:", msg="AoS code path is not available after QMCPACK v3.10.0")

    conflicts(
        "+phdf5",
        when="~mpi",
        msg="Parallel collective I/O requires MPI-enabled QMCPACK. "
        'Please add "~phdf5" to the Spack install line for serial QMCPACK.',
    )

    conflicts(
        "+soa",
        when="+cuda@:3.4.0",
        msg="QMCPACK CUDA+SOA variant does not exist prior to v. 3.5.0.",
    )

    conflicts("^openblas+ilp64", msg="QMCPACK does not support OpenBLAS 64-bit integer variant")

    conflicts("^openblas threads=none", msg="QMCPACK does not support OpenBLAS without threading")

    conflicts("^openblas threads=pthreads", msg="QMCPACK does not support OpenBLAS with pthreads")

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="A value for cuda_arch must be specified. Add cuda_arch=XX",
    )

    # Omitted for now due to concretizer bug
    # conflicts('^intel-mkl+ilp64',
    #           msg='QMCPACK does not support MKL 64-bit integer variant')

    # QMCPACK 3.15.0 increased the minimum gcc to 9
    conflicts("%gcc@:8", when="@3.15.0:")

    # QMCPACK 3.10.0 increased the minimum requirements for compiler versions
    newer_compiler_warning = (
        "QMCPACK v3.10.0 or later requires a newer " "version of this compiler"
    )
    conflicts("%gcc@:6", when="@3.10.0:", msg=newer_compiler_warning)
    conflicts("%intel@:18", when="@3.10.0:", msg=newer_compiler_warning)
    conflicts("%clang@:6", when="@3.10.0:", msg=newer_compiler_warning)

    # QMCPACK 3.6.0 or later requires support for C++14
    cpp14_warning = "QMCPACK v3.6.0 or later requires a " "compiler with support for C++14"
    conflicts("%gcc@:4", when="@3.6.0:", msg=cpp14_warning)
    conflicts("%intel@:17", when="@3.6.0:", msg=cpp14_warning)
    conflicts("%pgi@:17", when="@3.6.0:", msg=cpp14_warning)
    conflicts("%clang@:3.4", when="@3.6.0:", msg=cpp14_warning)

    conflicts("+afqmc", when="@:3.6.0", msg="AFQMC not recommended before v3.7")
    conflicts("+afqmc", when="~mpi", msg="AFQMC requires building with +mpi")
    conflicts("+afqmc", when="%gcc@:6.0", msg="AFQMC code requires gcc@6.1 or greater")
    conflicts("+afqmc", when="%apple-clang@:9.2", msg="AFQMC code requires clang 4.1 or greater")
    conflicts("+afqmc", when="%clang@:4.0", msg="AFQMC code requires clang 4.1 or greater")
    conflicts("+afqmc", when="%intel@:18", msg="AFQMC code requires intel19 or greater")

    # Prior to QMCPACK 3.5.0 Intel MKL was not properly detected with
    # non-Intel compilers without a Spack-based hack. This hack
    # had the potential for negative side effects and led to more
    # complex Python code that would have been difficult to maintain
    # long term. Note that this has not been an issue since QMCPACK 3.5.0.
    # For older versions of QMCPACK, we issue a conflict below if you
    # try to use Intel MKL with a non-Intel compiler.
    mkl_warning = (
        "QMCPACK releases prior to 3.5.0 require the "
        "Intel compiler when linking against Intel MKL"
    )
    conflicts("%gcc", when="@:3.4.0 ^intel-mkl", msg=mkl_warning)
    conflicts("%pgi", when="@:3.4.0 ^intel-mkl", msg=mkl_warning)
    conflicts("%llvm", when="@:3.4.0 ^intel-mkl", msg=mkl_warning)

    # Dependencies match those in the QMCPACK manual.
    # FIXME: once concretizer can unite unconditional and conditional
    # dependencies, some of the '~mpi' variants below will not be necessary.
    # Essential libraries
    depends_on("cmake@3.4.3:", when="@:3.5.0", type="build")
    depends_on("cmake@3.6.0:", when="@3.6.0:", type="build")
    depends_on("cmake@3.14.0:", when="@3.10.0:", type="build")
    depends_on("cmake@3.17.0:", when="@3.16.0:", type="build")
    depends_on("boost+exception+serialization+random", type="build")
    depends_on("boost@1.61.0:+exception+serialization+random", when="@3.6.0:", type="build")
    depends_on("libxml2")
    depends_on("mpi", when="+mpi")
    depends_on("python@3:", when="@3.9:")

    # HDF5
    depends_on("hdf5~mpi", when="~phdf5")
    depends_on("hdf5+mpi", when="+phdf5")

    # Math libraries
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api@3")

    # qmcpack data analysis tools
    # basic command line tool based on Python and NumPy
    # It may be necesseary to disable the blas and lapack
    # when building the 'py-numpy' package, but it should not be a hard
    # dependency on the 'py-numpy~blas~lapack' variant
    depends_on("py-numpy", when="+da", type="run")

    # GUI is optional for data anlysis
    # py-matplotlib leads to a long complex DAG for dependencies
    depends_on("py-matplotlib", when="+gui", type="run")

    # Backport several patches from recent versions of QMCPACK
    # The test_numerics unit test is broken prior to QMCPACK 3.3.0
    patch_url = "https://github.com/QMCPACK/qmcpack/pull/621.patch?full_index=1"
    patch_checksum = "54484b722df264dae3fd0c1094883b17431617e278eeba2cffbd720b36c9e21a"
    patch(patch_url, sha256=patch_checksum, when="@3.1.0:3.3.0")

    # FindMKL.cmake has an issues prior to QMCPACK 3.3.0
    patch_url = "https://github.com/QMCPACK/qmcpack/pull/623.patch?full_index=1"
    patch_checksum = "9e444d627ab22ad5f31797aec0c0d662463055955eff1c84fbde274e0259db6b"
    patch(patch_url, sha256=patch_checksum, when="@3.1.0:3.3.0")

    # git-rev files for not git builds issues prior to QMCPACK 3.3.0
    patch_url = "https://github.com/QMCPACK/qmcpack/pull/643.patch?full_index=1"
    patch_checksum = "d6410e7843f6c062bf9aa8ecf107e573b35c32022927d63f8cf5ad36ccf873c3"
    patch(patch_url, sha256=patch_checksum, when="@3.1.0:3.3.0")

    # the default flag_handler for Spack causes problems for QMCPACK
    # https://spack.readthedocs.io/en/latest/packaging_guide.html#the-build-environment:
    flag_handler = CMakePackage.build_system_flags

    @when("@:3.7.0")
    def patch(self):
        # FindLibxml2QMC.cmake doesn't check the environment by default
        # for libxml2, so we fix that.
        filter_file(
            r"$ENV{LIBXML2_HOME}/lib",
            "${LIBXML2_HOME}/lib $ENV{LIBXML2_HOME}/lib",
            "CMake/FindLibxml2QMC.cmake",
        )

    @property
    def build_targets(self):
        spec = self.spec
        targets = ["all"]
        if "+ppconvert" in spec:
            targets.append("ppconvert")

        return targets

    # QMCPACK prefers taking MPI compiler wrappers as CMake compilers.
    def setup_build_environment(self, env):
        spec = self.spec
        if "+mpi" in spec:
            env.set("CC", spec["mpi"].mpicc)
            env.set("CXX", spec["mpi"].mpicxx)

    def cmake_args(self):
        spec = self.spec
        args = []

        # This issue appears specifically with the the Intel compiler,
        # but may be an issue with other compilers as well. The final fix
        # probably needs to go into QMCPACK's CMake instead of in Spack.
        # QMCPACK binaries are linked with the C++ compiler, but *may* contain
        # Fortran libraries such as NETLIB-LAPACK and OpenBLAS on the link
        # line. For the case of the Intel C++ compiler, we need to manually
        # add a libray from the Intel Fortran compiler.
        if "%intel" in spec:
            args.append("-DQMC_EXTRA_LIBS=-lifcore")

        # Currently FFTW_HOME and LIBXML2_HOME are used by CMake.
        # Any CMake warnings about other variables are benign.
        # Starting with QMCPACK 3.8.0, CMake uses the builtin find(libxml2)
        # function
        if spec.satisfies("@:3.7.0"):
            xml2_prefix = spec["libxml2"].prefix
            args.append("-DLIBXML2_HOME={0}".format(xml2_prefix))
            args.append("-DLibxml2_INCLUDE_DIRS={0}".format(xml2_prefix.include))
            args.append("-DLibxml2_LIBRARY_DIRS={0}".format(xml2_prefix.lib))

        if "^fftw@3:" in spec:
            fftw_prefix = spec["fftw"].prefix
            args.append("-DFFTW_HOME={0}".format(fftw_prefix))
            args.append("-DFFTW_INCLUDE_DIRS={0}".format(fftw_prefix.include))
            args.append("-DFFTW_LIBRARY_DIRS={0}".format(fftw_prefix.lib))
        elif "^armpl-gcc" in spec:
            args.append("-DFFTW_LIBRARIES={0}".format(spec["armpl-gcc"].libs.joined(";")))
            args.append("-DFFTW_INCLUDE_DIR={0}".format(spec["armpl-gcc"].headers.directories[0]))
        elif "^acfl" in spec:
            args.append("-DFFTW_LIBRARIES={0}".format(spec["acfl"].libs.joined(";")))
            args.append("-DFFTW_INCLUDE_DIR={0}".format(spec["acfl"].headers.directories[0]))

        if "^armpl-gcc" in spec:
            args.append("-DBLAS_LIBRARIES={0}".format(spec["armpl-gcc"].libs.joined(";")))
        elif "^acfl" in spec:
            args.append("-DBLAS_LIBRARIES={0}".format(spec["acfl"].libs.joined(";")))

        args.append("-DBOOST_ROOT={0}".format(self.spec["boost"].prefix))
        args.append("-DHDF5_ROOT={0}".format(self.spec["hdf5"].prefix))

        # Default is MPI, serial version is convenient for cases, e.g. laptops
        if "+mpi" in spec:
            args.append("-DQMC_MPI=1")
        else:
            args.append("-DQMC_MPI=0")

        # Default is parallel collective I/O enabled
        if "+phdf5" in spec:
            args.append("-DENABLE_PHDF5=1")
        else:
            args.append("-DENABLE_PHDF5=0")

        # Default is real-valued single particle orbitals
        if "+complex" in spec:
            args.append("-DQMC_COMPLEX=1")
        else:
            args.append("-DQMC_COMPLEX=0")

        if "+afqmc" in spec:
            args.append("-DBUILD_AFQMC=1")
        else:
            args.append("-DBUILD_AFQMC=0")

        # When '-DQMC_CUDA=1', CMake automatically sets:
        # '-DQMC_MIXED_PRECISION=1'
        #
        # There is a double-precision CUDA path, but it is not as well
        # tested.

        if "+cuda" in spec:
            # Cannot support both CUDA builds at the same time, see
            # earlier notes in this package.
            if "+afqmc" in spec:
                args.append("-DENABLE_CUDA=1")
            else:
                args.append("-DQMC_CUDA=1")
            cuda_arch_list = spec.variants["cuda_arch"].value
            cuda_arch = cuda_arch_list[0]
            if len(cuda_arch_list) > 1:
                raise InstallError(
                    "QMCPACK only supports compilation for a single " "GPU architecture at a time"
                )
            if "@3.14.0:" in self.spec:
                args.append("-DCMAKE_CUDA_ARCHITECTURES={0}".format(cuda_arch))
            else:
                args.append("-DCUDA_ARCH=sm_{0}".format(cuda_arch))
        else:
            args.append("-DQMC_CUDA=0")

        # Mixed-precision versues double-precision CPU and GPU code
        if "+mixed" in spec:
            args.append("-DQMC_MIXED_PRECISION=1")
        else:
            args.append("-DQMC_MIXED_PRECISION=0")

        # New Structure-of-Array (SOA) code, much faster than default
        # Array-of-Structure (AOS) code.
        # No support for local atomic orbital basis.
        if "+soa" in spec:
            args.append("-DENABLE_SOA=1")
        else:
            args.append("-DENABLE_SOA=0")

        # Manual Timers
        if "+timers" in spec:
            args.append("-DENABLE_TIMERS=1")
        else:
            args.append("-DENABLE_TIMERS=0")

        # Proper detection of optimized BLAS and LAPACK.
        # Based on the code from the deal II Spack package:
        # https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/dealii/package.py
        #
        # Basically, we override CMake's auto-detection mechanism
        # and use the Spack's interface instead.
        #
        # For version of QMCPACK prior to 3.5.0, the lines
        # below are used for detection of all math libraries.
        # For QMCPACK 3.5.0 and later, the lines below are only
        # needed when MKL is *not* used. Thus, it is redundant
        # but there are no negative side effects.
        lapack_blas = spec["lapack"].libs + spec["blas"].libs
        args.extend(["-DLAPACK_FOUND=true", "-DLAPACK_LIBRARIES=%s" % lapack_blas.joined(";")])

        # Next two environment variables were introduced in QMCPACK 3.5.0
        # Prior to v3.5.0, these lines should be benign but CMake
        # may issue a warning.
        if spec["lapack"].name in INTEL_MATH_LIBRARIES:
            args.append("-DENABLE_MKL=1")
            args.append("-DMKL_ROOT=%s" % env["MKLROOT"])
        else:
            args.append("-DENABLE_MKL=0")

        # ppconvert is not build by default because it may exhibit numerical
        # issues on some systems
        if "+ppconvert" in spec:
            args.append("-DBUILD_PPCONVERT=1")
        else:
            args.append("-DBUILD_PPCONVERT=0")

        return args

    # QMCPACK needs custom install method for the following reason:
    # Note that 3.6.0 release and later has a functioning 'make install',
    # but still does not install nexus, manual, etc. So, there is no compelling
    # reason to use QMCPACK's built-in version at this time.
    def install(self, spec, prefix):
        # create top-level directory
        mkdirp(prefix)

        # We assume cwd is self.stage.source_path, then
        # install manual, labs, and nexus
        install_tree("labs", prefix.labs)
        install_tree("nexus", prefix.nexus)

        # install binaries
        with working_dir(self.build_directory):
            install_tree("bin", prefix.bin)

    def setup_run_environment(self, env):
        """Set-up runtime environment for QMCPACK.
        Set PATH and PYTHONPATH for basic analysis scripts for Nexus."""

        env.prepend_path("PATH", self.prefix.nexus.bin)
        env.prepend_path("PYTHONPATH", self.prefix.nexus.lib)

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Run ctest after building binary.
        It can take over 24 hours to run all the regression tests, here we
        only run the unit tests and deterministic tests. If the unit tests
        fail, the QMCPACK installation aborts. If the deterministic tests
        fails, QMCPACK will still install and emit a warning message."""

        with working_dir(self.build_directory):
            ctest("-R", "unit")
            try:
                ctest("-R", "deterministic", "-LE", "unstable")
            except ProcessError:
                warn = "Unit tests passed, but deterministic tests failed.\n"
                warn += "Please report this failure to:\n"
                warn += "https://github.com/QMCPACK/qmcpack/issues"
                tty.msg(warn)

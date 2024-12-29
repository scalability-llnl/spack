# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.store
from spack.package import *
from spack.pkg.builtin.boost import Boost


class Openspeedshop(CMakePackage):
    """OpenSpeedShop is a community effort led by Trenza, Inc.
    It builds on top of a broad list of community infrastructures,
    most notably Dyninst and MRNet from UW, libmonitor from Rice,
    and PAPI from UTK.  OpenSpeedShop is an open source multi platform
    Linux performance tool which is targeted to support performance
    analysis of applications running on both single node and large
    scale IA64, IA32, EM64T, AMD64, PPC, ARM, Power8, Intel Phi, Blue
    Gene and Cray platforms.  OpenSpeedShop development is hosted by
    Trenza Inc.. The infrastructure and base components of OpenSpeedShop
    are released as open source code primarily under LGPL.
    """

    homepage = "http://www.openspeedshop.org"
    git = "https://github.com/OpenSpeedShop/openspeedshop.git"

    maintainers("jgalarowicz")

    license("GPL-2.0-only")

    version("develop", branch="master")
    version("2.4.2.1", branch="2.4.2.1")
    version("2.4.2", branch="2.4.2")
    version("2.4.1", branch="2.4.1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "runtime", default=False, description="build only the runtime libraries and collectors."
    )
    variant(
        "crayfe",
        default=False,
        description="build only the FE tool using the runtime_dir \
                         to point to target build.",
    )
    variant("cuda", default=False, description="build with cuda packages included.")

    variant(
        "gui",
        default="none",
        values=("none", "qt3", "qt4"),
        description="Build or not build a GUI of choice",
    )

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    # MPI variants
    variant(
        "openmpi",
        default=False,
        description="Build mpi collector for openmpi \
                         MPI when variant is enabled.",
    )
    variant(
        "mpt",
        default=False,
        description="Build mpi collector for SGI \
                         MPT MPI when variant is enabled.",
    )
    variant(
        "mvapich2",
        default=False,
        description="Build mpi collector for mvapich2\
                         MPI when variant is enabled.",
    )
    variant(
        "mpich2",
        default=False,
        description="Build mpi collector for mpich2\
                         MPI when variant is enabled.",
    )

    depends_on("cmake@3.0.2:", type="build")

    # Dependencies for openspeedshop that are common to all
    # the variants of the OpenSpeedShop build
    depends_on("libtool", type="link")  # links against libltdl
    depends_on("bison", type="build")
    depends_on("flex@2.6.1", type="build")

    # For binutils
    depends_on("binutils@2.32")

    depends_on("elfutils", type="link")
    depends_on("libdwarf")

    depends_on("sqlite")

    # For boost
    depends_on("boost@1.70.0:")
    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    depends_on("dyninst@10:", when="@2.4.0:9999")

    depends_on("python", type=("build", "run"))

    depends_on("libxml2")

    depends_on("qt@3:3.9", when="gui=qt3")

    # Dependencies for the openspeedshop cbtf packages.
    depends_on("cbtf@develop", when="@develop", type=("build", "link", "run"))
    depends_on("cbtf@1.9.3:9999", when="@2.4.0:9999", type=("build", "link", "run"))

    depends_on("cbtf-krell@develop", when="@develop", type=("build", "link", "run"))
    depends_on("cbtf-krell@1.9.3:9999", when="@2.4.0:9999", type=("build", "link", "run"))

    depends_on("cbtf-krell@develop+crayfe", when="@develop+crayfe", type=("build", "link", "run"))
    depends_on(
        "cbtf-krell@1.9.3:9999+crayfe", when="@2.4.0:9999+crayfe", type=("build", "link", "run")
    )

    depends_on("cbtf-krell@develop+mpich2", when="@develop+mpich2", type=("build", "link", "run"))
    depends_on(
        "cbtf-krell@1.9.3:9999+mpich2", when="@2.4.0:9999+mpich2", type=("build", "link", "run")
    )

    depends_on("cbtf-krell@develop+mpt", when="@develop+mpt", type=("build", "link", "run"))
    depends_on("cbtf-krell@1.9.3:9999+mpt", when="@2.4.0:9999+mpt", type=("build", "link", "run"))

    depends_on(
        "cbtf-krell@develop+mvapich2", when="@develop+mvapich2", type=("build", "link", "run")
    )
    depends_on(
        "cbtf-krell@1.9.3:9999+mvapich2",
        when="@2.4.0:9999+mvapich2",
        type=("build", "link", "run"),
    )

    depends_on(
        "cbtf-krell@develop+openmpi", when="@develop+openmpi", type=("build", "link", "run")
    )
    depends_on(
        "cbtf-krell@1.9.3:9999+openmpi", when="@2.4.0:9999+openmpi", type=("build", "link", "run")
    )

    depends_on("cbtf-argonavis@develop", when="@develop+cuda", type=("build", "link", "run"))
    depends_on("cbtf-argonavis@1.9.3:9999", when="@2.4.0:9999+cuda", type=("build", "link", "run"))

    # For MRNet
    depends_on("mrnet@5.0.1-3:+lwthreads", when="@develop", type=("build", "link", "run"))
    depends_on("mrnet@5.0.1-3:+lwthreads", when="@2.4.0:9999", type=("build", "link", "run"))

    patch("arm.patch", when="target=aarch64:")
    parallel = False

    build_directory = "build_openspeedshop"

    def set_cray_login_node_cmake_options(self, spec, cmake_options):
        # Appends to cmake_options the options that will enable the appropriate
        # Cray login node libraries

        cray_login_node_options = []
        rt_platform = "cray"

        # How do we get the compute node (CNL) cbtf package install
        # directory path?
        # spec['cbtf'].prefix is the login node value for this build, as
        # we only get here when building the login node components and
        # that is all that is known to spack.
        store = spack.store
        be_ck = store.db.query_one("cbtf-krell arch=cray-CNL-haswell")

        # Equivalent to install-tool cmake arg:
        # '-DCBTF_KRELL_CN_RUNTIME_DIR=%s'
        #               % <base dir>/cbtf_v2.4.0.release/compute)
        cray_login_node_options.append("-DCBTF_KRELL_CN_RUNTIME_DIR=%s" % be_ck.prefix)
        cray_login_node_options.append("-DRUNTIME_PLATFORM=%s" % rt_platform)

        cmake_options.extend(cray_login_node_options)

    def cmake_args(self):
        spec = self.spec

        compile_flags = "-O2 -g -Wall"

        cmake_args = []

        # Indicate building cbtf vers (transfer rawdata files)
        instrumentor_setting = "cbtf"

        if spec.satisfies("+runtime"):
            # Appends base options to cmake_args
            self.set_defaultbase_cmake_options(spec, cmake_args)
            cmake_args.extend(
                [
                    "-DCMAKE_CXX_FLAGS=%s" % compile_flags,
                    "-DCMAKE_C_FLAGS=%s" % compile_flags,
                    "-DINSTRUMENTOR=%s" % instrumentor_setting,
                    "-DCBTF_DIR=%s" % spec["cbtf"].prefix,
                    "-DCBTF_KRELL_DIR=%s" % spec["cbtf-krell"].prefix,
                    "-DMRNET_DIR=%s" % spec["mrnet"].prefix,
                ]
            )

            if spec.satisfies("+cuda"):
                cmake_args.extend(["-DCBTF_ARGONAVIS_DIR=%s" % spec["cbtf-argonavis"].prefix])

        else:
            # Appends base options to cmake_args
            self.set_defaultbase_cmake_options(spec, cmake_args)
            guitype = self.spec.variants["gui"].value
            cmake_args.extend(
                [
                    "-DCMAKE_CXX_FLAGS=%s" % compile_flags,
                    "-DCMAKE_C_FLAGS=%s" % compile_flags,
                    "-DINSTRUMENTOR=%s" % instrumentor_setting,
                    "-DSQLITE3_DIR=%s" % spec["sqlite"].prefix,
                    "-DCBTF_DIR=%s" % spec["cbtf"].prefix,
                    "-DCBTF_KRELL_DIR=%s" % spec["cbtf-krell"].prefix,
                    "-DMRNET_DIR=%s" % spec["mrnet"].prefix,
                ]
            )

            if guitype == "none":
                cmake_args.extend(["-DBUILD_QT3_GUI=FALSE"])
            elif guitype == "qt4":
                cmake_args.extend(["-DBUILD_QT3_GUI=FALSE"])
            elif guitype == "qt3":
                cmake_args.extend(["-DQTLIB_DIR=%s" % spec["qt"].prefix])

            if spec.satisfies("+cuda"):
                cmake_args.extend(["-DCBTF_ARGONAVIS_DIR=%s" % spec["cbtf-argonavis"].prefix])

            if spec.satisfies("+crayfe"):
                # We need to build target/compute node
                # components/libraries first then pass
                # those libraries to the openspeedshop
                # login node build
                self.set_cray_login_node_cmake_options(spec, cmake_args)

        return cmake_args

    def set_defaultbase_cmake_options(self, spec, cmake_options):
        # Appends to cmake_options the options that will enable
        # the appropriate base level options to the openspeedshop
        # cmake build.
        cmake_options.extend(
            [
                self.define("BINUTILS_DIR", spec["binutils"].prefix),
                self.define("LIBELF_DIR", spec["elfutils"].prefix),
                self.define("LIBDWARF_DIR", spec["libdwarf"].prefix),
                self.define("Boost_NO_SYSTEM_PATHS", True),
                self.define("Boost_NO_BOOST_CMAKE", True),
                self.define("BOOST_ROOT", spec["boost"].prefix),
                self.define("Boost_DIR", spec["boost"].prefix),
                self.define("BOOST_LIBRARYDIR", spec["boost"].prefix.lib),
                self.define("DYNINST_DIR", spec["dyninst"].prefix),
            ]
        )

    def set_mpi_cmake_options(self, spec, cmake_options):
        # Appends to cmake_options the options that will enable
        # the appropriate MPI implementations

        mpi_options = []

        # openmpi
        if spec.satisfies("+openmpi"):
            mpi_options.append("-DOPENMPI_DIR=%s" % spec["openmpi"].prefix)
        # mpich
        if spec.satisfies("+mpich"):
            mpi_options.append("-DMPICH_DIR=%s" % spec["mpich"].prefix)
        # mpich2
        if spec.satisfies("+mpich2"):
            mpi_options.append("-DMPICH2_DIR=%s" % spec["mpich2"].prefix)
        # mvapich
        if spec.satisfies("+mvapich"):
            mpi_options.append("-DMVAPICH_DIR=%s" % spec["mvapich"].prefix)
        # mvapich2
        if spec.satisfies("+mvapich2"):
            mpi_options.append("-DMVAPICH2_DIR=%s" % spec["mvapich2"].prefix)
        # mpt
        if spec.satisfies("+mpt"):
            mpi_options.append("-DMPT_DIR=%s" % spec["mpt"].prefix)

        cmake_options.extend(mpi_options)

    def setup_run_environment(self, env):
        """Set up the compile and runtime environments for a package."""

        # Find Dyninst library path, this is needed to
        # set the DYNINSTAPI_RT_LIB library which is
        # required for OpenSpeedShop to find loop level
        # performance information
        dyninst_libdir = find_libraries(
            "libdyninstAPI_RT", root=self.spec["dyninst"].prefix, shared=True, recursive=True
        )

        # Set Dyninst RT library path to support OSS loop resolution code
        env.set("DYNINSTAPI_RT_LIB", dyninst_libdir[0])

        env.set("OPENSS_RAWDATA_DIR", ".")

        # Set the openspeedshop plugin path
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        plugin_path = "/openspeedshop"
        oss_plugin_path = lib_dir + plugin_path
        env.set("OPENSS_PLUGIN_PATH", oss_plugin_path)

        cbtf_mc = "/sbin/cbtf_mrnet_commnode"
        cbtf_lmb = "/sbin/cbtf_libcbtf_mrnet_backend"
        env.set("XPLAT_RSH", "ssh")
        env.set("MRNET_COMM_PATH", join_path(self.spec["cbtf-krell"].prefix + cbtf_mc))

        # Set CBTF_MPI_IMPLEMENTATON to the appropriate mpi implementation
        # This is needed by O|SS and CBTF tools to deploy the correct
        # mpi runtimes for ossmpi, ossmpit, ossmpip, and cbtfsummary
        # Users may have to set the CBTF_MPI_IMPLEMENTATION variable
        # manually if multiple mpi's are specified in the build
        if self.spec.satisfies("+mpich"):
            env.set("CBTF_MPI_IMPLEMENTATION", "mpich")

        if self.spec.satisfies("+mvapich"):
            env.set("CBTF_MPI_IMPLEMENTATION", "mvapich")

        if self.spec.satisfies("+mvapich2"):
            env.set("CBTF_MPI_IMPLEMENTATION", "mvapich2")

        if self.spec.satisfies("+mpt"):
            env.set("CBTF_MPI_IMPLEMENTATION", "mpt")

        if self.spec.satisfies("+openmpi"):
            env.set("CBTF_MPI_IMPLEMENTATION", "openmpi")

        env.set("CBTF_MRNET_BACKEND_PATH", join_path(self.spec["cbtf-krell"].prefix + cbtf_lmb))
        env.prepend_path("PATH", self.spec["mrnet"].prefix.bin)
        env.prepend_path("PATH", self.spec["cbtf-krell"].prefix.bin)
        env.prepend_path("PATH", self.spec["cbtf-krell"].prefix.sbin)
        mpath = "/share/man"
        env.prepend_path("MANPATH", self.spec["cbtf-krell"].prefix + mpath)
        env.prepend_path("PATH", self.spec["python"].prefix.bin)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os.path

from spack.package import *


class Plumed(AutotoolsPackage):
    """PLUMED is an open source library for free energy calculations in
    molecular systems which works together with some of the most popular
    molecular dynamics engines.

    Free energy calculations can be performed as a function of many order
    parameters with a particular focus on biological problems, using state
    of the art methods such as metadynamics, umbrella sampling and
    Jarzynski-equation based steered MD.

    The software, written in C++, can be easily interfaced with both fortran
    and C/C++ codes.
    """

    homepage = "https://www.plumed.org/"
    url = "https://github.com/plumed/plumed2/archive/v2.7.4.tar.gz"
    git = "https://github.com/plumed/plumed2.git"
    maintainers("marcodelapierre")

    license("LGPL-3.0-or-later")

    version("master", branch="master")

    version("2.9.2", sha256="301fbc958374f81d9b8c7a1eac73095f6dded52cce73ce33d64bdbebf51ac63d")
    version("2.9.1", sha256="e24563ad1eb657611918e0c978d9c5212340f128b4f1aa5efbd439a0b2e91b58")
    version("2.9.0", sha256="612d2387416b5f82dd8545709921440370e144fd46cef633654cf0ee43bac5f8")

    version("2.8.3", sha256="e98da486e252cdf290b0b5b2f3f021409ea0d2d775ab609a6ad68fc1ab143a3b")
    version("2.8.2", sha256="a2064bacba1dde36b05aaf351ba4b7e6d30a165b332b0a83b7a6db04b477be9f")
    version("2.8.1", sha256="f56bc9266c8a47241385c595717c2734a9b67148a7f4122b808bc0733710173e")
    version("2.8.0", sha256="8357eca6f280125037ad4e7c427f96f2af2f60ddfedce1a2e36e1e1cc3bff32b")

    version("2.7.6", sha256="9ca7b1e84bf2343a09a5b604222dd04aa0fc8b62a7cb82d1d68b795b6b189c06")
    version("2.7.5", sha256="39cb01108706df7ef71c7c315ddfc4306137f62ac72222b8582ab892221f7972")
    version("2.7.4", sha256="6f5dc16a753c71ed719f17f9cbb61642ab8e716fb7f77e22960dfa145c3b8211")
    version("2.7.3", sha256="aa1f6200c2ed351e40ce4391a9590f171532474b30f384feddfab10e36d7e08e")
    version("2.7.2", sha256="c9a31e68d6440828cf186ca43c9e11a5e5c7ad1c96b2b66ed5a5a141fc954373")
    version("2.7.1", sha256="cb8b5735d8dd61980fa6441f3dde3f33544240ae4177da0f529fb5abb355cd4a")
    version("2.7.0", sha256="14450ea566c25ac9bf71fd77bb9c0c95e9038462b5739c73a515be82e2011cd6")

    version("2.6.6", sha256="43a7bb410280141c020363671c685a759d4497b3db3eb3c04899264b51a26859")
    version("2.6.5", sha256="3b72587ba6fe72def46bcc7d917974123279879de7f8335acf542bba57865eed")
    version("2.6.4", sha256="53e49c0db6cc769d238834bea884e856f4e7bb8f71c9929e5584bd977113f03b")
    version("2.6.3", sha256="d05b9e4a4c1329fc932d5bdd04f20419be230f98159bdc012a91716461ab4a2f")
    version("2.6.2", sha256="bbc2ef0cb08d404513b8b737c72333b6656389e15effd6a0f9ace2a5758c9a4a")
    version("2.6.1", sha256="c1b3c397b2d971140aa240dde50e48a04ce78e3dedb02b6dca80fa53f8026e4e")
    version("2.6.0", sha256="3d57ae460607a49547ef38a52c4ac93493a3966857c352280a9c05f5dcdb1820")

    version("2.5.7", sha256="aa10d2879c3edeaef9d5a530fe8b05f67ecfbec2e9423e0f95701d0bc54826c7")
    version("2.5.6", sha256="1bc29b0274196fb553cdf7ba8ecb7a93a91d60a920d99863edbcd536d618ce8c")
    version("2.5.5", sha256="70faa9ff1938e286dc388cb793b39840953e5646855b684f48df1bc864b737e8")
    version("2.5.4", sha256="a1647e598191f261e75d06351e607475d395af481315052a4c28563ac9989a7f")
    version("2.5.3", sha256="543288be667dc4201fc461ecd2dd4878ddfbeac682d0c021c99ea8e501c7c9dc")
    version("2.5.2", sha256="85d10cc46e2e37c7719cf51c0931278f56c2c8f8a9d86188b2bf97c2535a2ab4")
    version("2.5.1", sha256="de309980dcfd6f6e0e70e138856f4bd9eb4d8a513906a5e6389f18a5af7f2eba")
    version("2.5.0", sha256="53e08187ec9f8af2326fa84407e34644a7c51d2af93034309fb70675eee5e4f7")

    # These versions don't build in CI.
    version(
        "2.4.6",
        sha256="c22ad19f5cd36ce9fe4ba0b53158fc2a3d985c48fc04606e3f3b3e835b994cb3",
        deprecated=True,
    )
    version(
        "2.4.4",
        sha256="1e5c24109314481fad404da97d61c7339b219e27e120c9c80bacc79c9f6a51a8",
        deprecated=True,
    )
    version(
        "2.4.2",
        sha256="528ce57f1f5330480bcd403140166a4580efd2acaea39c85dfeca5e2cd649321",
        deprecated=True,
    )
    version(
        "2.4.1",
        sha256="f00410ebdd739c2ddf55fcd714ff4bd88a1029e02d2fc9cea0b5fca34e0fc4eb",
        deprecated=True,
    )

    version(
        "2.3.5",
        sha256="a6a66ca4582c1aecc6138c96be015e13cd06a718e8446b2f13e610fe34602e4f",
        deprecated=True,
    )
    version(
        "2.3.3",
        sha256="ac058ff529f207d5b4169fb5a87bdb3c77307dfef1ac543ad8b6c74c5de7fc91",
        deprecated=True,
    )
    version(
        "2.3.0",
        sha256="b1c8a54a313a0569e27e36420770074f35406453f73de70e55c424652abeddf1",
        deprecated=True,
    )

    version(
        "2.2.4",
        sha256="d7a1dba34a7fe03f23e8d39ab6e15b230c4851373fdceb3602e2de26ea53ce37",
        deprecated=True,
    )
    version(
        "2.2.3",
        sha256="2db19c5f6a2918833941d0bf47b5431d0865529d786df797ccc966d763ed7b0c",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Variants. PLUMED by default builds a number of optional modules.
    # The ones listed here are not built by default for various reasons,
    # such as stability, lack of testing, or lack of demand.
    #
    # From 'configure --help' @2.3:
    # all/none/reset or : separated list such as
    # +crystallization:-bias default: reset
    #
    # Optional modules can be provided in two ways, via the `optional_modules` variant:
    # 1. Use a reference set of optional modules via `optional_modules` (recommended).
    #    Allowed values are: `all`[default], `reset`.
    # 2. Pick any combination of specific optional modules (advanced).
    #    Only the requested optional modules will be activated.
    #    See list in variable `single_optional_modules` below.
    #    This list comes from the Plumed manual, eg for 2.8:
    #    https://www.plumed.org/doc-v2.8/user-doc/html/mymodules.html
    # These are implemented using multi-valued variants (`disjoint_sets`),
    # and the `conditional` option to handle version conflicts.
    single_optional_modules = (
        conditional("adjmat", when="@2.3:"),
        "analysis",
        conditional("annfunc", when="@2.6:"),
        "bias",
        "cltools",
        "colvar",
        "crystallization",
        conditional("dimred", when="@2.5:"),
        conditional("drr", when="@2.4:"),
        conditional("eds", when="@2.4:"),
        conditional("fisst", when="@2.7:"),
        "function",
        conditional("funnel", when="@2.7:"),
        "generic",
        conditional("imd", when="@:2.2.99"),
        conditional("isdb", when="@2.4:"),
        conditional("logmfd", when="@2.5:"),
        "manyrestraints",
        "mapping",
        conditional("maze", when="@2.6:"),
        "molfile",
        "multicolvar",
        conditional("opes", when="@2.7:"),
        conditional("pamm", when="@2.5: optional_modules=adjmat"),
        conditional("piv", when="@2.5:"),
        conditional("reference", when="@:2.2.99"),
        conditional("s2cm", when="@2.8:"),
        conditional("sasa", when="@2.8:"),
        "secondarystructure",
        "setup",
        "vatom",
        conditional("ves", when="@2.4:"),
        conditional("vesselbase", when="@:2.2.99"),
        conditional("xdrfile", when="@2.8:"),
    )

    variant(
        "optional_modules",
        values=disjoint_sets(("all",), ("reset",), single_optional_modules)
        .prohibit_empty_set()
        .with_default("all"),
        description="Activates optional modules: all, reset, or custom list (advanced)",
    )

    variant("shared", default=True, description="Builds shared libraries")
    variant("mpi", default=True, description="Activates MPI support")
    variant("gsl", default=True, description="Activates GSL support")
    variant(
        "arrayfire",
        default="none",
        values=("none", "cpu", "cuda", "opencl"),
        description="Activates FireArray support",
    )

    # Dependencies. LAPACK and BLAS are recommended but not essential.
    depends_on("zlib-api")
    depends_on("blas")
    depends_on("lapack")
    # For libmatheval support through the 'function' module
    # which is enabled by default (or when optional_modules=all)
    depends_on("libmatheval", when="@:2.4")
    depends_on("arrayfire", when="arrayfire=cpu")
    depends_on("arrayfire+cuda", when="arrayfire=cuda")
    depends_on("arrayfire+opencl", when="arrayfire=opencl")

    depends_on("mpi", when="+mpi")
    depends_on("gsl", when="+gsl")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("py-cython", type="build", when="@2.5:")

    force_autoreconf = True

    parallel = False

    def apply_patch(self, other):
        # The name of MD engines differ slightly from the ones used in Spack
        format_strings = collections.defaultdict(lambda: "{0.name}-{0.version}")
        format_strings["espresso"] = "q{0.name}-{0.version}"
        format_strings["amber"] = "{0.name}{0.version}"

        get_md = lambda x: format_strings[x.name].format(x)

        # Get available patches
        plumed_patch = Executable(os.path.join(self.spec.prefix.bin, "plumed-patch"))

        out = plumed_patch("-q", "-l", output=str)
        available = out.split(":")[-1].split()

        # Check that `other` is among the patchable applications
        if get_md(other) not in available:
            msg = "{0.name}@{0.version} is not among the MD engine"
            msg += " that can be patched by {1.name}@{1.version}.\n"
            msg += "Supported engines are:\n"
            for x in available:
                msg += x + "\n"
            raise RuntimeError(msg.format(other, self.spec))

        # Call plumed-patch to patch executables
        target = format_strings[other.name].format(other)
        plumed_patch("-p", "-e", target)

    def setup_dependent_package(self, module, dependent_spec):
        # Make plumed visible from dependent packages
        module.plumed = dependent_spec["plumed"].command

    @property
    def plumed_inc(self):
        return os.path.join(self.prefix.lib, "plumed", "src", "lib", "Plumed.inc")

    @run_before("autoreconf")
    def filter_gslcblas(self):
        # This part is needed to avoid linking with gsl cblas
        # interface which will mask the cblas interface
        # provided by optimized libraries due to linking order
        filter_file("-lgslcblas", "", "configure.ac")

    @when("@2.5:")
    def patch(self):
        # Ensure Spack's wrappers are used to compile the Python interface
        env = (
            'CC="{0}" LDSHARED="{0} -pthread -shared" '
            'CXX="{1}" LDCXXSHARED="{1} -pthread -shared"'.format(spack_cc, spack_cxx)
        )
        filter_file(
            "plumed_program_name=plumed",
            "{0} plumed_program_name=plumed".format(env),
            "src/lib/Makefile",
            "python/Makefile",
        )

    def configure_args(self):
        spec = self.spec

        # From plumed docs :
        # Also consider that this is different with respect to what some other
        # configure script does in that variables such as MPICXX are
        # completely ignored here. In case you work on a machine where CXX is
        # set to a serial compiler and MPICXX to a MPI compiler, to compile
        # with MPI you should use:
        #
        # > ./configure CXX="$MPICXX"

        # The configure.ac script may detect the wrong linker for
        # LD_RO which causes issues at link time. Here we work around
        # the issue saying we have no LD_RO executable.
        configure_opts = ["--disable-ld-r"]

        # If using MPI then ensure the correct compiler wrapper is used.
        if "+mpi" in spec:
            configure_opts.extend(["--enable-mpi", "CXX={0}".format(spec["mpi"].mpicxx)])

            # If the MPI dependency is provided by the intel-mpi package then
            # the following additional argument is required to allow it to
            # build.
            if "intel-mpi" in spec:
                configure_opts.extend(["STATIC_LIBS=-mt_mpi"])

        extra_libs = []
        # Set flags to help find gsl
        if "+gsl" in spec:
            gsl_libs = spec["gsl"].libs
            blas_libs = spec["blas"].libs
            extra_libs.append((gsl_libs + blas_libs).ld_flags)
        # Set flags to help with ArrayFire
        if "arrayfire=none" not in spec:
            libaf = "arrayfire:{0}".format(spec.variants["arrayfire"].value)
            extra_libs.append(spec[libaf].libs.search_flags)

        if extra_libs:
            configure_opts.append("LDFLAGS={0}".format(" ".join(extra_libs)))

        # Additional arguments
        configure_opts.extend(
            [
                "--enable-shared={0}".format("yes" if "+shared" in spec else "no"),
                "--enable-gsl={0}".format("yes" if "+gsl" in spec else "no"),
                "--enable-af_cpu={0}".format("yes" if "arrayfire=cpu" in spec else "no"),
                "--enable-af_cuda={0}".format("yes" if "arrayfire=cuda" in spec else "no"),
                "--enable-af_ocl={0}".format("yes" if "arrayfire=ocl" in spec else "no"),
            ]
        )

        # Construct list of optional modules
        optional_modules = self.spec.variants["optional_modules"].value
        # Predefined set of modules
        if "all" in optional_modules:
            selected_modules = "all"
        elif "reset" in optional_modules:
            selected_modules = "reset"
        # Custom set of modules
        else:
            selected_modules = "none"
            for mod in optional_modules:
                selected_modules += ":+{0}".format(mod)
        configure_opts.append("--enable-modules={0}".format(selected_modules))

        return configure_opts

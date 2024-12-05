# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Unifyfs(AutotoolsPackage):
    """User level file system that enables applications to use node-local
    storage as burst buffers for shared files. Supports scalable and efficient
    aggregation of I/O bandwidth from burst buffers while having the same life
    cycle as a batch-submitted job.
    UnifyFS is designed to support common I/O workloads, including
    checkpoint/restart. While primarily designed for N-N write/read, UnifyFS
    compliments its functionality with the support for N-1 write/read."""

    homepage = "https://github.com/LLNL/UnifyFS"
    git = "https://github.com/LLNL/UnifyFS.git"
    url = "https://github.com/LLNL/UnifyFS/releases/download/v1.1/unifyfs-1.1.tar.gz"
    maintainers("CamStan")

    tags = ["e4s"]

    version("develop", branch="dev")
    version("2.0", sha256="a07dfda022bc3094d578dcc5c9b2c4bbe7de479f598e4e358cd01690cd82355b")
    version("1.1", sha256="1bf5593099d272c9a12c46090d217c61dfeea1504dd4f7184972da3db5afc5f3")
    version("1.0.1", sha256="d92800778661b15ab50275c4efe345a6c60d8f1802a0d5909fda38db91b12116")
    version("1.0", sha256="c9ad0d15d382773841a3dab89c661fbdcfd686ec37fa263eb22713f6404258f5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "auto-mount",
        default=True,
        description="Enable automatic mount/unmount in MPI_Init/Finalize",
    )
    variant(
        "boostsys",
        default=False,
        description="Have Mercury use preprocessor headers from boost dependency",
    )
    variant("fortran", default=True, description="Build with gfortran support")
    variant("pmi", default=False, description="Enable PMI2 build options")
    variant("pmix", default=False, description="Enable PMIx build options")
    variant(
        "preload",
        default=False,
        when="@1.0.1:",
        description="Enable support for LD_PRELOAD library",
    )
    variant("spath", default=True, description="Use spath library to normalize relative paths")

    depends_on("autoconf", type="build")
    depends_on("automake@1.15:", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    # Required dependencies
    depends_on("gotcha@1.0.4:")
    depends_on("mochi-margo@0.9.6:0.9.9", when="@1.0:1.0.1")
    # Version 1.1 mostly tested on mochi-margo@0.13.1. Leaving this all
    # inclusive from v0.10 on until any bugs are reported on versions before or
    # after v0.13.1.
    depends_on("mochi-margo@0.10:", when="@1.1:")
    depends_on("mpi")

    # unifyfs@:1.1 uses MD5 functions that are deprecated in OpenSSL 3,these
    # were removed in release 2.0.
    depends_on("openssl@:3")

    # Mochi-Margo dependencies
    depends_on("mercury@2.1", when="^mochi-margo@0.9.6:0.9.9")
    depends_on("mercury~boostsys", when="~boostsys")
    depends_on("libfabric fabrics=rxm,sockets,tcp", when="^mercury@2:+ofi")

    # Optional dependencies
    depends_on("spath~mpi", when="+spath")

    conflicts("^libfabric@1.13:1.13.1")
    conflicts("^mercury~bmi~ofi")
    conflicts("^mercury~sm")
    # Known compatibility issues with ifort and xlf. Fixes coming.
    conflicts("%intel", when="+fortran")
    conflicts("%xl", when="+fortran")

    debug_build = False
    build_directory = "spack-build"

    # Only builds properly with debug symbols when flag_handler =
    # build_system_flags.
    # Override the default behavior in order to set debug_build which is used
    # to set the --disable-silent-rules option when configuring.
    def flag_handler(self, name, flags):
        if name in ("cflags", "cppflags"):
            if "-g" in flags:
                self.debug_build = True
        if name == "cflags":
            if self.spec.satisfies("%oneapi@2022.2.0:"):
                flags.append("-Wno-error=deprecated-non-prototype")
                flags.append("-Wno-error=unused-function")
            if self.spec.satisfies("%gcc@4"):
                flags.append("-std=gnu99")
        return (None, None, flags)

    def setup_build_environment(self, env):
        # GCC11 generates a bogus array bounds error:
        # See https://gcc.gnu.org/bugzilla/show_bug.cgi?id=98266
        if "%gcc@11" in self.spec:
            env.append_flags("CFLAGS", "-Wno-array-bounds")
        if self.spec.satisfies("%oneapi"):
            env.append_flags("CFLAGS", "-Wno-unused-function")

    @when("%cce@11.0.3:")
    def patch(self):
        filter_file("-Werror", "", "client/src/Makefile.in")
        filter_file("-Werror", "", "client/src/Makefile.am")

    @when("@develop")
    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    def configure_args(self):
        spec = self.spec
        args = ["--with-gotcha=%s" % spec["gotcha"].prefix]

        args.extend(self.with_or_without("spath", activation_value="prefix"))
        args.extend(self.enable_or_disable("mpi-mount", variant="auto-mount"))
        args.extend(self.enable_or_disable("fortran"))
        args.extend(self.enable_or_disable("pmi"))
        args.extend(self.enable_or_disable("pmix"))
        args.extend(self.enable_or_disable("preload"))

        if self.debug_build:
            args.append("--disable-silent-rules")
        else:
            args.append("--enable-silent-rules")

        return args

    def check(self):
        with working_dir(self.build_directory):
            make("check", parallel=False)

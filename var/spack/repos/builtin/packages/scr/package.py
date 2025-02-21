# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


def detect_scheduler():
    if which("aprun"):
        return "APRUN"
    if which("flux"):
        return "FLUX"
    if which("jsrun"):
        return "LSF"
    return "SLURM"


class Scr(CMakePackage):
    """SCR caches checkpoint data in storage on the compute nodes of a
    Linux cluster to provide a fast, scalable checkpoint/restart
    capability for MPI codes"""

    homepage = "https://computing.llnl.gov/projects/scalable-checkpoint-restart-for-mpi"
    url = "https://github.com/LLNL/scr/archive/v1.2.0.tar.gz"
    git = "https://github.com/llnl/scr.git"
    tags = ["e4s", "radiuss"]

    maintainers("CamStan", "gonsie")

    version("develop", branch="develop")
    version("legacy", branch="legacy")

    version(
        "3.1.0",
        sha256="ca1f37c84e0ff7a307e68f213c8cc868974d7fb30f16826853a711c7c3a55ffa",
        preferred=True,
    )
    version("3.0.1", sha256="ba8f9e676aec8176ecc46c31a4f470ac95047101654de8cc88e01a1f9d95665a")
    version("3.0.0", sha256="e204d3e99a49efac50b4bedc7ac05f55a05f1a65429500d919900c82490532cc")
    version("2.0.0", sha256="471978ae0afb56a20847d3989b994fbd680d1dea21e77a5a46a964b6e3deed6b")
    version(
        "1.2.2",
        sha256="764a85638a9e8762667ec1f39fa5f7da7496fca78de379a22198607b3e027847",
        deprecated=True,
    )
    version(
        "1.2.1",
        sha256="23acab2dc7203e9514455a5168f2fd57bc590affb7a1876912b58201513628fe",
        deprecated=True,
    )
    version(
        "1.2.0",
        sha256="e3338ab2fa6e9332d2326c59092b584949a083a876adf5a19d4d5c7a1bbae047",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("zlib-api")

    # Use latest iteration of dtcmp and  components when installing scr@develop
    cmpnts = ["axl", "dtcmp", "er", "kvtree", "rankstr", "redset", "shuffile", "spath"]
    for comp in cmpnts:
        depends_on(comp + "@main", when="@develop")

    # SCR legacy is anything 2.x.x or earlier
    # SCR components is anything 3.x.x or later
    with when("@3.1.0"):
        depends_on("axl@0.8.0: +mpi")
        depends_on("er@0.5.0")
        depends_on("kvtree@1.4.0:")
        depends_on("rankstr@0.3.0:")
        depends_on("redset@0.4.0")
        depends_on("shuffile@0.3.0:")
        depends_on("spath@0.3.0: +mpi")
        depends_on("dtcmp@1.1.5")

    with when("@3.0.1"):
        depends_on("axl@0.7.1 +mpi")
        depends_on("er@0.3.0")

    with when("@3.0.0"):
        depends_on("axl@0.6.0")
        depends_on("er@0.2.0")

    with when("@3.0.0:3.0.1"):
        depends_on("kvtree@1.3.0")
        depends_on("rankstr@0.2.0")
        depends_on("redset@0.2.0")
        depends_on("shuffile@0.2.0")
        depends_on("spath@0.2.0 +mpi")
        depends_on("dtcmp@1.1.4:")

    # DTCMP is an optional dependency up until 3.x, required thereafter
    variant(
        "dtcmp",
        default=True,
        when="@:2",
        description="Build with DTCMP. " "Necessary to enable user directory naming at runtime",
    )
    depends_on("dtcmp", when="+dtcmp")
    depends_on("dtcmp", when="@3:")

    variant(
        "libyogrt", default=True, description="Build SCR with libyogrt for get_time_remaining."
    )
    depends_on("libyogrt scheduler=slurm", when="+libyogrt resource_manager=SLURM")
    depends_on("libyogrt scheduler=flux", when="+libyogrt resource_manager=FLUX")
    depends_on("libyogrt scheduler=lsf", when="+libyogrt resource_manager=LSF")
    depends_on("libyogrt", when="+libyogrt")

    # PDSH required up to 3.0rc1, optional thereafter
    # TODO spack currently assumes 3.0.0 = 3.0 = 3 < 3.0rc1 < 3.0rc2
    variant("pdsh", default=True, when="@3:", description="Enable use of PDSH")
    depends_on("pdsh+static_modules", type=("build", "run"), when="+pdsh")
    depends_on("pdsh+static_modules", type=("build", "run"), when="@:2")

    variant(
        "scr_config",
        default="scr.conf",
        description="Location for SCR to find its system config file. "
        "May be either absolute or relative to the install prefix",
    )
    variant(
        "copy_config",
        default="none",
        description="Location from which to copy SCR system config file. "
        "Must be an absolute path.",
    )

    variant("fortran", default=True, description="Build SCR with fortran bindings")

    variant(
        "resource_manager",
        default=detect_scheduler(),
        values=("SLURM", "APRUN", "FLUX", "LSF", "NONE"),
        multi=False,
        description="Resource manager for which to configure SCR.",
    )

    # SCR_ASYNC_API only used in :2.x.x
    variant(
        "async_api",
        default="NONE",
        when="@:2",
        values=("NONE", "CRAY_DW", "IBM_BBAPI", "INTEL_CPPR"),
        multi=False,
        description="Asynchronous data transfer API to use with SCR.",
    )

    variant("pthreads", default=True, when="@3:", description="Enable Pthread support")
    depends_on("axl+pthreads", when="+pthreads")

    variant("bbapi", default=False, when="@3:", description="Enable IBM BBAPI support")
    depends_on("axl+bbapi", when="+bbapi")
    depends_on("axl~bbapi", when="~bbapi")

    variant(
        "bbapi_fallback",
        default=False,
        when="@3: +bbapi",
        description="Using BBAPI, if source or destination don't support "
        "file extents then fallback to pthreads",
    )
    depends_on("axl+bbapi+bbapi_fallback", when="@3: +bbapi_fallback")

    variant("dw", default=False, when="@3:", description="Enable Cray DataWarp support")
    depends_on("axl+dw", when="+dw")
    depends_on("axl~dw", when="~dw")

    variant("examples", default=True, when="@3:", description="Build SCR example programs")

    variant(
        "file_lock",
        default="FLOCK",
        values=("FLOCK", "FNCTL", "NONE"),
        multi=False,
        description="File locking style for SCR.",
    )
    depends_on("kvtree file_lock=FLOCK", when="@3: file_lock=FLOCK")
    depends_on("kvtree file_lock=FNCTL", when="@3: file_lock=FNCTL")
    depends_on("kvtree file_lock=NONE", when="@3: file_lock=NONE")

    # Enabling SCR logging is a WIP, for which this will be needed
    # MySQL currently having build issues
    # variant('mysql', default=False, description='Build with MySQL to allow for '
    #         'capturing SCR and syslog messages in a database')
    # depends_on('mysql', when='+mysql')

    variant("shared", default=True, when="@3:", description="Build with shared libraries")
    depends_on("libyogrt+static", when="~shared")
    for comp in cmpnts:
        depends_on(comp + "+shared", when="+shared")
        depends_on(comp + "~shared", when="~shared")
    conflicts("~shared", when="+bbapi", msg="See SCR issue #453")
    conflicts("~shared", when="+examples", msg="See SCR issue #455")

    # TODO: Expose `tests` and `resource_manager` variants in components and
    # then propogate their setting through components.
    variant("tests", default=True, when="@3:", description="Build with CTest included")

    # The default cache and control directories should be placed in tmpfs if available.
    # On Linux, /dev/shm is a common tmpfs location.  Other platforms, like macOS,
    # do not define a common tmpfs location, so /tmp is the next best option.
    platform_tmp_default = "/dev/shm" if sys.platform == "linux" else "/tmp"
    variant(
        "cache_base",
        default=platform_tmp_default,
        description="Compile time default location for cache directory.",
    )
    variant(
        "cntl_base",
        default=platform_tmp_default,
        description="Compile time default location for control directory.",
    )

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%cce"):
            if name in ["cflags", "cxxflags", "cppflags"]:
                return (None, flags, None)
            elif name == "ldflags":
                flags.append("-ldl")
        return (flags, None, None)

    def get_abs_path_rel_prefix(self, path):
        # Return path if absolute, otherwise prepend prefix
        if os.path.isabs(path):
            return path
        else:
            return join_path(self.spec.prefix, path)

    def cmake_args(self):
        spec = self.spec
        args = []

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("ENABLE_FORTRAN", "fortran"))
        args.append(self.define_from_variant("ENABLE_IBM_BBAPI", "bbapi"))
        args.append(self.define_from_variant("ENABLE_CRAY_DW", "dw"))
        args.append(self.define_from_variant("ENABLE_EXAMPLES", "examples"))
        args.append(self.define_from_variant("ENABLE_YOGRT", "libyogrt"))
        # args.append(self.define_from_variant('ENABLE_MYSQL', 'mysql'))
        args.append(self.define_from_variant("ENABLE_PDSH", "pdsh"))
        args.append(self.define_from_variant("ENABLE_PTHREADS", "pthreads"))
        args.append(self.define_from_variant("ENABLE_TESTS", "tests"))
        args.append(self.define_from_variant("SCR_ASYNC_API", "async_api"))
        args.append(self.define_from_variant("SCR_FILE_LOCK", "file_lock"))
        args.append(self.define_from_variant("SCR_CACHE_BASE", "cache_base"))
        args.append(self.define_from_variant("SCR_CNTL_BASE", "cntl_base"))
        args.append(self.define_from_variant("SCR_RESOURCE_MANAGER", "resource_manager"))
        args.append(
            self.define(
                "SCR_CONFIG_FILE", self.get_abs_path_rel_prefix(spec.variants["scr_config"].value)
            )
        )

        if "+libyogrt" in spec:
            args.append(self.define("WITH_YOGRT_PREFIX", spec["libyogrt"].prefix))

        # if '+mysql' in spec:
        #    args.append(self.define('WITH_MYSQL_PREFIX', spec['mysql'].prefix))

        if spec.satisfies("@3:"):
            # DTCMP and components required from this point on
            cmpnts = ["axl", "dtcmp", "er", "kvtree", "rankstr", "redset", "shuffile", "spath"]
            for comp in cmpnts:
                args.append(self.define("WITH_" + comp.upper() + "_PREFIX", spec[comp].prefix))

            # PDSH optional from this point on
            if "+pdsh" in spec:
                args.append(self.define("WITH_PDSH_PREFIX", spec["pdsh"].prefix))
        else:
            # dtcmp optional before this point
            if "+dtcmp" in spec:
                args.append(self.define("WITH_DTCMP_PREFIX", spec["dtcmp"].prefix))

            # PDSH required before this point
            args.append(self.define("WITH_PDSH_PREFIX", spec["pdsh"].prefix))

        return args

    @run_after("install")
    def copy_config(self):
        spec = self.spec
        if spec.variants["copy_config"].value != "none":
            dest_path = self.get_abs_path_rel_prefix(spec.variants["scr_config"].value)
            install(spec.variants["copy_config"].value, dest_path)

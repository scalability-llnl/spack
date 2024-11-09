# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import os
import sys

from llnl.util.lang import dedupe

import spack.builder
from spack.build_systems import autotools, cmake
from spack.package import *
from spack.util.environment import filter_system_paths


class NetcdfC(CMakePackage, AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the C distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    git = "https://github.com/Unidata/netcdf-c.git"
    url = "https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.8.1.tar.gz"

    maintainers("skosukhin", "WardF")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("4.9.2", sha256="bc104d101278c68b303359b3dc4192f81592ae8640f1aee486921138f7f88cb7")
    version("4.9.0", sha256="9f4cb864f3ab54adb75409984c6202323d2fc66c003e5308f3cdf224ed41c0a6")
    version("4.8.1", sha256="bc018cc30d5da402622bf76462480664c6668b55eb16ba205a0dfb8647161dd0")
    version("4.8.0", sha256="aff58f02b1c3e91dc68f989746f652fe51ff39e6270764e484920cb8db5ad092")
    version("4.7.4", sha256="99930ad7b3c4c1a8e8831fb061cb02b2170fc8e5ccaeda733bd99c3b9d31666b")
    version("4.7.3", sha256="05d064a2d55147b83feff3747bea13deb77bef390cb562df4f9f9f1ce147840d")
    version("4.7.2", sha256="7648db7bd75fdd198f7be64625af7b276067de48a49dcdfd160f1c2ddff8189c")
    version("4.7.1", sha256="583e6b89c57037293fc3878c9181bb89151da8c6015ecea404dd426fea219b2c")
    version("4.7.0", sha256="26d03164074363b3911ed79b7cddd045c22adf5ebaf978943db11a1d9f15e9d3")
    version("4.6.3", sha256="734a629cdaed907201084d003cfa091806d6080eeffbd4204e7c7f73ff9d3564")
    version("4.6.2", sha256="673936c76ae0c496f6dde7e077f5be480afc1e300adb2c200bf56fbe22e5a82a")
    version("4.6.1", sha256="a2fabf27c72a5ee746e3843e1debbaad37cd035767eaede2045371322211eebb")
    version("4.6.0", sha256="6d740356399aac12290650325a05aec2fe92c1905df10761b2b0100994197725")
    version("4.5.0", sha256="f7d1cb2a82100b9bf9a1130a50bc5c7baf0de5b5022860ac3e09a0a32f83cf4a")
    # Version 4.4.1.1 is having problems in tests
    #    https://github.com/Unidata/netcdf-c/issues/343
    version("4.4.1.1", sha256="7f040a0542ed3f6d27f3002b074e509614e18d6c515b2005d1537fec01b24909")
    # Version 4.4.1 can crash on you (in real life and in tests).  See:
    #    https://github.com/Unidata/netcdf-c/issues/282
    version("4.4.1", sha256="17599385fd76ccdced368f448f654de2ed000fece44dece9fb5d598798b4c9d6")
    version("4.4.0", sha256="09b78b152d3fd373bee4b5738dc05c7b2f5315fe34aa2d94ee9256661119112f")
    version("4.3.3.1", sha256="f2ee78eb310637c007f001e7c18e2d773d23f3455242bde89647137b7344c2e2")
    version("4.3.3", sha256="3f16e21bc3dfeb3973252b9addf5defb48994f84fc9c9356081f871526a680e7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    with when("build_system=cmake"):
        # TODO: document why we need to revert https://github.com/Unidata/netcdf-c/pull/1731
        #  with the following patch:
        patch("4.8.1-win-hdf5-with-zlib.patch", when="@4.8.1: platform=windows")

        # TODO: https://github.com/Unidata/netcdf-c/pull/2595 contains some of the changes
        # made in this patch but is not sufficent to replace the patch. There is currently
        # no upstream PR (or set of PRs) covering all changes in this path.
        # When #2595 lands, this patch should be updated to include only
        # the changes not incorporated into that PR
        patch("netcdfc_correct_and_export_link_interface.patch")

    # Some of the patches touch configure.ac and, therefore, require forcing the autoreconf stage:
    _force_autoreconf_when = []
    with when("build_system=autotools"):
        # See https://github.com/Unidata/netcdf-c/pull/1752
        patch(
            "https://github.com/Unidata/netcdf-c/commit/386e2695286702156eba27ab7c68816efb192230.patch?full_index=1",
            sha256="cb928a91f87c1615a0788f95b95d7a2e3df91dc16822f8b8a34a85d4e926c0de",
            when="@4.7.3:4.7.4 +parallel-netcdf",
        )
        _force_autoreconf_when.append("@4.7.3:4.7.4 +parallel-netcdf")

        # See https://github.com/Unidata/netcdf-c/pull/2293
        patch(
            "https://github.com/Unidata/netcdf-c/commit/a7ea050ebb3c412a99cc352859d5176a9b5ef986.patch?full_index=1",
            sha256="38d34de38bad99737d3308867071196f20a3fb39b936de7bfcfbc85eb0c7ef54",
            when="@4.8.1",
        )
        _force_autoreconf_when.append("@4.8.1")

        # See https://github.com/Unidata/netcdf-c/pull/2710
        # Versions 4.9.0 and 4.9.1 had a bug in the configure script, which worked to our benefit.
        # The bug has been fixed in
        # https://github.com/Unidata/netcdf-c/commit/267b26f1239310ca7ba8304315834939f7cc9886 and
        # now we need a patch in cases when we build for macOS with DAP disabled:
        patch(
            "https://github.com/Unidata/netcdf-c/commit/cfe6231aa6b018062b443cbe2fd9073f15283344.patch?full_index=1",
            sha256="4e105472de95a1bb5d8b0b910d6935ce9152777d4fe18b678b58347fa0122abc",
            when="@4.9.2~dap platform=darwin",
        )
        _force_autoreconf_when.append("@4.9.2~dap platform=darwin")

    with when("@4.7.2"):
        # Fix headers
        # See https://github.com/Unidata/netcdf-c/pull/1505
        patch(
            "https://github.com/Unidata/netcdf-c/pull/1505.patch?full_index=1",
            sha256="495b3e5beb7f074625bcec2ca76aebd339e42719e9c5ccbedbdcc4ffb81a7450",
        )
        # See https://github.com/Unidata/netcdf-c/pull/1508
        patch(
            "https://github.com/Unidata/netcdf-c/pull/1508.patch?full_index=1",
            sha256="19e7f31b96536928621b1c29bb6d1a57bcb7aa672cea8719acf9ac934cdd2a3e",
        )

    # See https://github.com/Unidata/netcdf-c/pull/2618
    patch(
        "https://github.com/Unidata/netcdf-c/commit/00a722b253bae186bba403d0f92ff1eba719591f.patch?full_index=1",
        sha256="25b83de1e081f020efa9e21c94c595220849f78c125ad43d8015631d453dfcb9",
        when="@4.9.0:4.9.1~mpi+parallel-netcdf",
    )

    # See https://github.com/Unidata/netcdf-c/issues/2674
    patch(
        "https://github.com/Unidata/netcdf-c/commit/f8904d5a1d89420dde0f9d2c0e051ba08d08e086.patch?full_index=1",
        sha256="0161eb870fdfaf61be9d70132c9447a537320342366362e76b8460c823bf95ca",
        when="@4.9.0:4.9.2",
    )

    variant("mpi", default=True, description="Enable parallel I/O for netcdf-4")
    variant("parallel-netcdf", default=False, description="Enable parallel I/O for classic files")
    variant("hdf4", default=False, description="Enable HDF4 support")
    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("shared", default=True, description="Enable shared library")
    variant("dap", default=False, description="Enable DAP support")
    variant("byterange", default=False, description="Enable byte-range I/O")
    variant("jna", default=False, description="Enable JNA support")
    variant("fsync", default=False, description="Enable fsync support")
    variant("nczarr_zip", default=False, description="Enable NCZarr zipfile format storage")
    variant("optimize", default=True, description="Enable -O2 for a more optimized lib")
    variant("logging", default=False, description="Enable logging")

    variant("szip", default=True, description="Enable Szip compression plugin")
    variant("blosc", default=True, description="Enable Blosc compression plugin")
    variant("zstd", default=True, description="Enable Zstandard compression plugin")

    with when("build_system=cmake"):
        # Based on the versions required by the root CMakeLists.txt:
        depends_on("cmake@2.8.12:", type="build", when="@4.3.3:4.3")
        depends_on("cmake@2.8.11:", type="build", when="@4.4.0:")
        depends_on("cmake@3.6.1:", type="build", when="@4.5.0:")
        depends_on("cmake@3.12:", type="build", when="@4.9.0:")
        # Starting version 4.9.1, nczarr_test/CMakeLists.txt relies on the FILE_PERMISSIONS feature
        # of the configure_file command, which is only available starting CMake 3.20:
        depends_on("cmake@3.20:", type="test", when="@4.9.1:")

    with when("build_system=autotools"):
        for __s in itertools.chain(["@main"], _force_autoreconf_when):
            with when(__s):
                depends_on("autoconf", type="build")
                depends_on("automake", type="build")
                depends_on("libtool", type="build")
                depends_on("m4", type="build")
        del __s

    # M4 is also needed for the source and man file generation. All the generated source files are
    # included in the release tarballs starting at least the oldest supported version:
    depends_on("m4", type="build", when="@main")

    # The man files are included in the release tarballs starting version 4.5.0 but they are not
    # needed for the Windows platform:
    for __p in ["darwin", "linux"]:
        with when("platform={0}".format(__p)):
            # It is possible to install the package with CMake and without M4 on a non-Windows
            # platform but some of the man files will not be installed in that case (even if they
            # are in the release tarball):
            depends_on("m4", type="build", when="build_system=cmake")
            # Apart from the redundant configure-time check, which we suppress below, M4 is not
            # needed when building with Autotools if the man files are in the release tarball:
            depends_on("m4", type="build", when="@:4.4 build_system=autotools")
    del __p

    depends_on("hdf~netcdf", when="+hdf4")

    # curl 7.18.0 or later is required:
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html
    depends_on("curl@7.18.0:", when="+dap")
    depends_on("curl@7.18.0:", when="+byterange")

    # Need to include libxml2 when using DAP in 4.9.0 and newer to build
    # https://github.com/Unidata/netcdf-c/commit/53464e89635a43b812b5fec5f7abb6ff34b9be63
    depends_on("libxml2", when="@4.9.0:+dap")

    depends_on("parallel-netcdf", when="+parallel-netcdf")

    # We need to build with MPI wrappers if any of the two
    # parallel I/O features is enabled:
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html#build_parallel
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+parallel-netcdf")

    # We also need to use MPI wrappers when building against static MPI-enabled HDF5:
    depends_on("mpi", when="^hdf5+mpi~shared")

    # High-level API of HDF5 1.8.9 or later is required for netCDF-4 support:
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html
    depends_on("hdf5@1.8.9:+hl")

    # Starting version 4.4.0, it became possible to disable parallel I/O even
    # if HDF5 supports it. For previous versions of the library we need
    # HDF5 without mpi support to disable parallel I/O:
    depends_on("hdf5~mpi", when="@:4.3~mpi")

    # We need HDF5 with mpi support to enable parallel I/O.
    depends_on("hdf5+mpi", when="+mpi")

    # NetCDF 4.4.0 and prior have compatibility issues with HDF5 1.10 and later
    # https://github.com/Unidata/netcdf-c/issues/250
    depends_on("hdf5@:1.8", when="@:4.4.0")

    # NetCDF 4.7.4 and prior require HDF5 1.10 or older
    # https://github.com/Unidata/netcdf-c/pull/1671
    depends_on("hdf5@:1.10", when="@:4.7.3")

    # Although NetCDF 4.8.0 builds and passes the respective tests against HDF5 1.12.0 with the
    # default API (i.e. the problem reported in https://github.com/Unidata/netcdf-c/issues/1965 is
    # not reproducible), the configure script fails if HDF5 1.12.0 is built without api=v18
    # (according to the error message emitted by the configure script) or api=v110 (according to
    # the comments in the configure script and its implementation). The check that led to the
    # failure was removed in version 4.8.1 (https://github.com/Unidata/netcdf-c/pull/2044). To
    # keep it simple, we require HDF5 1.10.x or older:
    depends_on("hdf5@:1.10", when="@4.8.0")

    with when("+byterange"):
        # HDF5 implements H5allocate_memory starting version 1.8.15:
        depends_on("hdf5@1.8.15:")
        # HDF5 defines H5FD_FEAT_DEFAULT_VFD_COMPATIBLE (required when version 1.10.x is used)
        # starting version 1.10.2:
        depends_on("hdf5@:1.9,1.10.2:")
        # The macro usage was adjusted (required when versions 1.8.23+, 1.10.8+, 1.12.1+ and
        # 1.13.0+ of HDF5 are used) in NetCDF 4.8.1
        # (see https://github.com/Unidata/netcdf-c/pull/2034):
        depends_on("hdf5@:1.8.22,1.10.0:1.10.7,1.12.0,1.13:", when="@:4.8.0")
        # Compatibility with HDF5 1.14.x was introduced in NetCDF 4.9.2
        # (see https://github.com/Unidata/netcdf-c/pull/2615):
        depends_on("hdf5@:1.12", when="@:4.9.1")

    depends_on("libzip", when="+nczarr_zip")

    # According to the documentation (see
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html), zlib 1.2.5 or
    # later is required for netCDF-4 compression. However, zlib became a direct dependency only
    # starting NetCDF 4.9.0 (for the deflate plugin):
    depends_on("zlib-api", when="@4.9.0:+shared")
    depends_on("zlib@1.2.5:", when="^[virtuals=zlib-api] zlib")

    # Use the vendored bzip2 on Windows:
    for __p in ["darwin", "linux"]:
        depends_on("bzip2", when="@4.9.0:+shared platform={0}".format(__p))
    del __p

    depends_on("szip", when="+szip")
    depends_on("c-blosc", when="+blosc")
    depends_on("zstd", when="+zstd")

    # Byte-range I/O was added in version 4.7.0:
    conflicts("+byterange", when="@:4.6")

    # NCZarr was added in version 4.8.0 as an experimental feature and became a supported one in
    # version 4.8.1:
    conflicts("+nczarr_zip", when="@:4.8.0")

    # The features were introduced in version 4.9.0:
    with when("@:4.8"):
        conflicts("+szip")
        conflicts("+blosc")
        conflicts("+zstd")

    # The plugins are not built when the shared libraries are disabled:
    with when("~shared"):
        conflicts("+szip")
        conflicts("+blosc")
        conflicts("+zstd")

    default_build_system = "cmake" if sys.platform == "win32" else "autotools"

    build_system("cmake", "autotools", default=default_build_system)

    def setup_run_environment(self, env):
        if self.spec.satisfies("@4.9.0:+shared"):
            # Both HDF5 and NCZarr backends honor the same environment variable:
            env.append_path("HDF5_PLUGIN_PATH", self.prefix.plugins)

    def flag_handler(self, name, flags):
        if self.builder.build_system == "autotools":
            if name == "cflags":
                if "+pic" in self.spec:
                    flags.append(self.compiler.cc_pic_flag)
                if "+optimize" in self.spec:
                    flags.append("-O2")
        return flags, None, None

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libnetcdf", root=self.prefix, shared=shared, recursive=True)


class BaseBuilder(metaclass=spack.builder.PhaseCallbacksMeta):
    def setup_dependent_build_environment(self, env, dependent_spec):
        # Some packages, e.g. ncview, refuse to build if the compiler path returned by nc-config
        # differs from the path to the compiler that the package should be built with. Therefore,
        # we have to shadow nc-config from self.prefix.bin, which references the real compiler,
        # with a backed up version, which references Spack compiler wrapper.
        if os.path.exists(self._nc_config_backup_dir):
            env.prepend_path("PATH", self._nc_config_backup_dir)

    @property
    def _nc_config_backup_dir(self):
        return join_path(self.pkg.metadata_dir, "spack-nc-config")

    @run_after("install")
    def backup_nc_config(self):
        # We expect this to be run before filter_compiler_wrappers:
        nc_config_file = self.prefix.bin.join("nc-config")
        if os.path.exists(nc_config_file):
            mkdirp(self._nc_config_backup_dir)
            install(nc_config_file, self._nc_config_backup_dir)

    filter_compiler_wrappers("nc-config", relative_root="bin")


class CMakeBuilder(BaseBuilder, cmake.CMakeBuilder):
    def cmake_args(self):
        base_cmake_args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_BYTERANGE", "byterange"),
            self.define("BUILD_UTILITIES", True),
            self.define("ENABLE_NETCDF_4", True),
            self.define_from_variant("ENABLE_DAP", "dap"),
            self.define_from_variant("ENABLE_HDF4", "hdf4"),
            self.define("ENABLE_PARALLEL_TESTS", False),
            self.define_from_variant("ENABLE_FSYNC", "fsync"),
            self.define("ENABLE_LARGE_FILE_SUPPORT", True),
            self.define_from_variant("NETCDF_ENABLE_LOGGING", "logging"),
        ]
        if "+parallel-netcdf" in self.pkg.spec:
            base_cmake_args.append(self.define("ENABLE_PNETCDF", True))
        if self.pkg.spec.satisfies("@4.3.1:"):
            base_cmake_args.append(self.define("ENABLE_DYNAMIC_LOADING", True))
        if "platform=windows" in self.pkg.spec:
            # Enforce the usage of the vendored version of bzip2 on Windows:
            base_cmake_args.append(self.define("Bz2_INCLUDE_DIRS", ""))
        if "+shared" in self.pkg.spec["hdf5"]:
            base_cmake_args.append(self.define("NC_FIND_SHARED_LIBS", True))
        else:
            base_cmake_args.append(self.define("NC_FIND_SHARED_LIBS", False))
        return base_cmake_args

    @run_after("install")
    def patch_hdf5_pkgconfigcmake(self):
        """
        Incorrect hdf5 library names are put in the package config files
        due to incorrectly using hdf5 target names
        https://github.com/spack/spack/pull/42878
        """
        if sys.platform == "win32":
            return

        pkgconfig_file = find(self.prefix, "netcdf.pc", recursive=True)
        ncconfig_file = find(self.prefix, "nc-config", recursive=True)
        settingsconfig_file = find(self.prefix, "libnetcdf.settings", recursive=True)

        files = pkgconfig_file + ncconfig_file + settingsconfig_file
        config = "shared" if self.spec.satisfies("+shared") else "static"
        filter_file(f"hdf5-{config}", "hdf5", *files, ignore_absent=True)
        filter_file(f"hdf5_hl-{config}", "hdf5_hl", *files, ignore_absent=True)


class AutotoolsBuilder(BaseBuilder, autotools.AutotoolsBuilder):
    @property
    def force_autoreconf(self):
        return any(self.spec.satisfies(s) for s in self.pkg._force_autoreconf_when)

    @when("@4.6.3:")
    def autoreconf(self, pkg, spec, prefix):
        if not os.path.exists(self.configure_abs_path):
            Executable("./bootstrap")()

    def configure_args(self):
        config_args = [
            "--enable-v2",
            "--enable-utilities",
            "--enable-static",
            "--enable-largefile",
            "--enable-netcdf-4",
        ]

        # NCZarr was added in version 4.8.0 as an experimental feature and became a supported one
        # in version 4.8.1:
        if self.spec.satisfies("@4.8.1:"):
            config_args.append("--enable-nczarr")
        elif self.spec.satisfies("@4.8.0"):
            config_args.append("--disable-nczarr")

        if self.spec.satisfies("@4.9.0:+shared"):
            # The plugins are not built when the shared libraries are disabled:
            config_args.extend(
                ["--enable-plugins", "--with-plugin-dir={0}".format(self.prefix.plugins)]
            )

        # The option was introduced in version 4.3.1 and does nothing starting version 4.6.1:
        if self.spec.satisfies("@4.3.1:4.6.0"):
            config_args.append("--enable-dynamic-loading")

        if self.spec.satisfies("@4.4:"):
            config_args += self.enable_or_disable("parallel4", variant="mpi")

        config_args += self.enable_or_disable("pnetcdf", variant="parallel-netcdf")

        config_args += self.enable_or_disable("hdf4")

        config_args += self.enable_or_disable("shared")

        config_args += self.enable_or_disable("dap")
        if self.spec.satisfies("@4.9.0:"):
            # Prevent linking to system libxml2:
            config_args += self.enable_or_disable("libxml2", variant="dap")

        if "+byterange" in self.spec:
            config_args.append("--enable-byterange")
        elif self.spec.satisfies("@4.7.0:"):
            config_args.append("--disable-byterange")

        if self.spec.satisfies("@4.3.2:"):
            config_args += self.enable_or_disable("jna")

        config_args += self.enable_or_disable("fsync")

        config_args += self.enable_or_disable("logging")

        if any(self.spec.satisfies(s) for s in ["+mpi", "+parallel-netcdf", "^hdf5+mpi~shared"]):
            config_args.append("CC={0}".format(self.spec["mpi"].mpicc))

        # In general, we rely on the compiler wrapper to inject the required CPPFLAGS and LDFLAGS.
        # However, the injected LDFLAGS are invisible for the configure script and are added
        # neither to the pkg-config nor to the nc-config files. Therefore, we generate LDFLAGS
        # based on the contents of the following list and pass them to the configure script:
        lib_search_dirs = []

        # In general, we rely on the configure script to generate the required linker flags in the
        # right order. However, the configure script does not know and does not check for several
        # possible transitive dependencies and we have to pass them as the LIBS argument. The list
        # is generated based on the contents of the following list:
        extra_libs = []

        if "+parallel-netcdf" in self.spec:
            lib_search_dirs.extend(self.spec["parallel-netcdf"].libs.directories)

        if "+hdf4" in self.spec:
            hdf = self.spec["hdf"]
            lib_search_dirs.extend(hdf.libs.directories)
            # The configure script triggers unavoidable overlinking to jpeg:
            lib_search_dirs.extend(hdf["jpeg"].libs.directories)
            if "~shared" in hdf:
                # We do not use self.spec["hdf:transitive"].libs to avoid even more duplicates
                # introduced by the configure script:
                if "+szip" in hdf:
                    extra_libs.append(hdf["szip"].libs)
                if "+external-xdr ^libtirpc" in hdf:
                    extra_libs.append(hdf["rpc"].libs)
                extra_libs.append(hdf["zlib-api"].libs)

        hdf5 = self.spec["hdf5:hl"]
        lib_search_dirs.extend(hdf5.libs.directories)
        if "~shared" in hdf5:
            if "+szip" in hdf5:
                extra_libs.append(hdf5["szip"].libs)
            extra_libs.append(hdf5["zlib-api"].libs)

        if self.spec.satisfies("@4.9.0:+shared"):
            lib_search_dirs.extend(self.spec["zlib-api"].libs.directories)
        else:
            # Prevent overlinking to zlib:
            config_args.append("ac_cv_search_deflate=")

        if "+nczarr_zip" in self.spec:
            lib_search_dirs.extend(self.spec["libzip"].libs.directories)
        elif self.spec.satisfies("@4.9.2:"):
            # Prevent linking to libzip to disable the feature:
            config_args.append("ac_cv_search_zip_open=no")
        elif self.spec.satisfies("@4.8.0:"):
            # Prevent linking to libzip to disable the feature:
            config_args.append("ac_cv_lib_zip_zip_open=no")

        if "+szip" in self.spec:
            lib_search_dirs.extend(self.spec["szip"].libs.directories)
        elif self.spec.satisfies("@4.9.0:"):
            # Prevent linking to szip to disable the plugin:
            config_args.append("ac_cv_lib_sz_SZ_BufftoBuffCompress=no")

        if self.spec.satisfies("@4.9.0:"):
            if "+shared" in self.spec:
                lib_search_dirs.extend(self.spec["bzip2"].libs.directories)
            else:
                # Prevent redundant entries mentioning system bzip2 in nc-config and pkg-config
                # files:
                config_args.append("ac_cv_lib_bz2_BZ2_bzCompress=no")

        if "+zstd" in self.spec:
            lib_search_dirs.extend(self.spec["zstd"].libs.directories)
        elif self.spec.satisfies("@4.9.0:"):
            # Prevent linking to system zstd:
            config_args.append("ac_cv_lib_zstd_ZSTD_compress=no")

        if "+blosc" in self.spec:
            lib_search_dirs.extend(self.spec["c-blosc"].libs.directories)
        elif self.spec.satisfies("@4.9.0:"):
            # Prevent linking to system c-blosc:
            config_args.append("ac_cv_lib_blosc_blosc_init=no")

        if self.spec.satisfies("@:4.7~dap+byterange"):
            extra_libs.append(self.spec["curl"].libs)
        elif "+dap" in self.spec or "+byterange" in self.spec:
            lib_search_dirs.extend(self.spec["curl"].libs.directories)
        elif self.spec.satisfies("@4.7.0"):
            # This particular version fails if curl is not found, even if it is not needed
            # (see https://github.com/Unidata/netcdf-c/issues/1390). Note that the following does
            # not trigger linking to system curl for this version because DAP support is disabled:
            config_args.append("ac_cv_lib_curl_curl_easy_setopt=yes")
        else:
            # Prevent linking to system curl (for versions 4.8.0 and newer) and the redundant check
            # for curl (for older versions):
            config_args.append("ac_cv_lib_curl_curl_easy_setopt=no")

        if not self.spec.satisfies("@:4.4,main"):
            # Suppress the redundant check for m4:
            config_args.append("ac_cv_prog_NC_M4=false")

        lib_search_dirs.extend(d for libs in extra_libs for d in libs.directories)
        # Remove duplicates and system prefixes:
        lib_search_dirs = filter_system_paths(dedupe(lib_search_dirs))
        config_args.append(
            "LDFLAGS={0}".format(" ".join("-L{0}".format(d) for d in lib_search_dirs))
        )

        extra_lib_names = [n for libs in extra_libs for n in libs.names]
        # Remove duplicates in the reversed order:
        extra_lib_names = reversed(list(dedupe(reversed(extra_lib_names))))
        config_args.append("LIBS={0}".format(" ".join("-l{0}".format(n) for n in extra_lib_names)))

        return config_args

    # It looks like the issues with running the tests in parallel were fixed around version 4.6.0
    # (see https://github.com/Unidata/netcdf-c/commit/812c2fd4d108cca927582c0d84049c0f271bb9e0):
    @when("@:4.5.0")
    def check(self):
        # h5_test fails when run in parallel
        make("check", parallel=False)

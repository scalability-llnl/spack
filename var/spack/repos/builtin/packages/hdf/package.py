# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Hdf(AutotoolsPackage):
    """HDF4 (also known as HDF) is a library and multi-object
    file format for storing and managing data between machines."""

    homepage = "https://portal.hdfgroup.org"
    url = "https://support.hdfgroup.org/ftp/HDF/releases/HDF4.2.14/src/hdf-4.2.14.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/HDF/releases/"
    list_depth = 2
    maintainers("lrknox")

    version("4.2.15", sha256="dbeeef525af7c2d01539906c28953f0fdab7dba603d1bc1ec4a5af60d002c459")
    version("4.2.14", sha256="2d383e87c8a0ca6a5352adbd1d5546e6cc43dc21ff7d90f93efa644d85c0b14a")
    version("4.2.13", sha256="be9813c1dc3712c2df977d4960e1f13f20f447dfa8c3ce53331d610c1f470483")
    version("4.2.12", sha256="dd419c55e85d1a0e13f3ea5ed35d00710033ccb16c85df088eb7925d486e040c")
    version("4.2.11", sha256="c3f7753b2fb9b27d09eced4d2164605f111f270c9a60b37a578f7de02de86d24")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("szip", default=False, description="Enable szip support")
    variant(
        "external-xdr", default=sys.platform != "darwin", description="Use an external XDR backend"
    )
    variant("netcdf", default=False, description="Build NetCDF API (version 2.3.2)")
    variant("fortran", default=False, description="Enable Fortran interface")
    variant("java", default=False, description="Enable Java JNI interface")
    variant("shared", default=False, description="Enable shared library")
    variant("pic", default=True, description="Produce position-independent code")

    depends_on("zlib-api")
    depends_on("jpeg")
    depends_on("szip", when="+szip")
    depends_on("rpc", when="+external-xdr")

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("java@7:", when="+java", type=("build", "run"))

    # https://forum.hdfgroup.org/t/cant-build-hdf-4-2-14-with-jdk-11-and-enable-java/5702
    patch("disable_doclint.patch", when="@:4.2.14^java@9:")

    conflicts("^libjpeg@:6a")

    # configure: error: Cannot build shared fortran libraries.
    # Please configure with --disable-fortran flag.
    conflicts("+fortran", when="+shared")

    # configure: error: Java requires shared libraries to be built
    conflicts("+java", when="~shared")

    # configure: WARNING: unrecognized options: --enable-java
    conflicts("+java", when="@:4.2.11")

    # The Java interface library uses netcdf-related macro definitions even
    # when netcdf is disabled and the macros are not defined, e.g.:
    # hdfsdsImp.c:158:30: error: 'MAX_NC_NAME' undeclared
    conflicts("+java", when="@4.2.12:4.2.13~netcdf")

    # TODO: '@:4.2.14 ~external-xdr' and the fact that we compile for 64 bit
    #  architecture should be in conflict

    # https://github.com/knedlsepp/nixpkgs/commit/c1a2918c849a5bc766c6d55d96bc6cf85c9d27f4
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-ppc.patch?full_index=1",
        sha256="5434f29a87856aa05124c7a9409b3ec3106c30b1ad722720773623190f6bfda8",
        when="@4.2.15:",
    )
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-4.2.4-sparc.patch?full_index=1",
        sha256="ce75518cccbeb80ab976b299225ea6104c3eec1ec13c09e2289913279fcf1b39",
        when="@4.2.15:",
    )
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-s390.patch?full_index=1",
        sha256="f7d67e8c3d0dad8bfca308936c6ac917cc0b63222c6339a29efdce14e8be6475",
        when="@4.2.15:",
    )
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-arm.patch?full_index=1",
        sha256="d54592df281c92e7e655b8312d18bef9ed096848de9430510e0699e98246ccd3",
        when="@4.2.15:",
    )
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-aarch64.patch?full_index=1",
        sha256="49733dd6143be7b30a28d386701df64a72507974274f7e4c0a9e74205510ea72",
        when="@4.2.15:",
    )
    # https://github.com/NOAA-EMC/spack-stack/issues/317
    patch("hdfi_h_apple_m1.patch", when="@4.2.15: target=aarch64: platform=darwin")

    @property
    def libs(self):
        """HDF can be queried for the following parameters:

        - "shared": shared libraries (default if '+shared')
        - "static": static libraries (default if '~shared')
        - "transitive": append transitive dependencies to the list of static
            libraries (the argument is ignored if shared libraries are
            requested)

        :return: list of matching libraries
        """
        libraries = ["libmfhdf", "libdf"]

        query_parameters = self.spec.last_query.extra_parameters

        if "shared" in query_parameters:
            shared = True
        elif "static" in query_parameters:
            shared = False
        else:
            shared = self.spec.satisfies("+shared")

        libs = find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

        if not libs:
            msg = "Unable to recursively locate {0} {1} libraries in {2}"
            raise spack.error.NoLibrariesError(
                msg.format("shared" if shared else "static", self.spec.name, self.spec.prefix)
            )

        if not shared and "transitive" in query_parameters:
            libs += self.spec["jpeg:transitive"].libs
            libs += self.spec["zlib:transitive"].libs
            if self.spec.satisfies("+szip"):
                libs += self.spec["szip:transitive"].libs
            if self.spec.satisfies("+external-xdr") and self.spec["rpc"].name == "libtirpc":
                libs += self.spec["rpc:transitive"].libs

        return libs

    def flag_handler(self, name, flags):
        if self.spec.satisfies("+pic"):
            if name == "cflags":
                flags.append(self.compiler.cc_pic_flag)
            elif name == "fflags":
                flags.append(self.compiler.f77_pic_flag)

        if name == "cflags":
            # https://forum.hdfgroup.org/t/help-building-hdf4-with-clang-error-implicit-declaration-of-function-test-mgr-szip-is-invalid-in-c99/7680
            if (
                self.spec.satisfies("@:4.2.15 %apple-clang")
                or self.spec.satisfies("%clang@16:")
                or self.spec.satisfies("%oneapi")
            ):
                flags.append("-Wno-error=implicit-function-declaration")

            if self.spec.satisfies("%clang@16:") or self.spec.satisfies("%apple-clang@15:"):
                flags.append("-Wno-error=implicit-int")

        return flags, None, None

    def configure_args(self):
        config_args = [
            "--enable-production",
            "--enable-static",
            "--with-zlib=%s" % self.spec["zlib-api"].prefix,
            "--with-jpeg=%s" % self.spec["jpeg"].prefix,
        ]

        config_args += self.enable_or_disable("shared")
        config_args += self.enable_or_disable("netcdf")
        config_args += self.enable_or_disable("fortran")
        config_args += self.enable_or_disable("java")

        if self.spec.satisfies("+szip"):
            config_args.append("--with-szlib=%s" % self.spec["szip"].prefix)
        else:
            config_args.append("--without-szlib")

        if self.spec.satisfies("~external-xdr"):
            config_args.append("--enable-hdf4-xdr")
        elif self.spec["rpc"].name == "libtirpc":
            # We should not specify '--disable-hdf4-xdr' due to a bug in the
            # configure script.
            config_args.append("LIBS=%s" % self.spec["rpc"].libs.link_flags)
            config_args.append("LDFLAGS=%s" % self.spec["rpc"].libs.search_flags)

        # https://github.com/Parallel-NetCDF/PnetCDF/issues/61
        if self.spec.satisfies("%gcc@10:"):
            config_args.extend(
                ["FFLAGS=-fallow-argument-mismatch", "FCFLAGS=-fallow-argument-mismatch"]
            )

        return config_args

    # Otherwise, we randomly get:
    # SDgetfilename:
    #   incorrect file being opened - expected <file755>, retrieved <file754>
    def check(self):
        with working_dir(self.build_directory):
            make("check", parallel=False)

    extra_install_tests = join_path("hdf", "util", "testfiles")

    # Filter h4cc compiler wrapper to substitute the Spack compiler
    # wrappers with the path of the underlying compilers.
    filter_compiler_wrappers("h4cc", relative_root="bin")

    @property
    def cached_tests_work_dir(self):
        """The working directory for cached test sources."""
        return join_path(self.test_suite.current_test_cache_dir, self.extra_install_tests)

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, self.extra_install_tests)

    def _check_version_match(self, exe):
        """Ensure exe version check yields spec version."""
        path = join_path(self.prefix.bin, exe)
        if not os.path.isfile(path):
            raise SkipTest(f"{exe} is not installed")

        exe = which(path)
        out = exe("-V", output=str.split, error=str.split)
        vers = f"Version {self.spec.version.up_to(2)}"
        assert vers in out

    def test_hdfimport_version(self):
        """ensure hdfimport version matches spec"""
        self._check_version_match("hdfimport")

    def test_hrepack_version(self):
        """ensure hrepack version matches spec"""
        self._check_version_match("hrepack")

    def test_ncdump_version(self):
        """ensure ncdump version matches spec"""
        self._check_version_match("hrepack")

    def test_ncgen_version(self):
        """ensure ncgen version matches spec"""
        self._check_version_match("ncgen")

    def test_gif_converters(self):
        """test image conversion sequence and diff"""
        base_name = "storm110"
        storm_fn = join_path(self.cached_tests_work_dir, f"{base_name}.hdf")
        if not os.path.exists(storm_fn):
            raise SkipTest(f"Missing test image {storm_fn}")

        if not os.path.exists(self.prefix.bin.hdf2gif) or not os.path.exists(
            self.prefix.bin.gif2hdf
        ):
            raise SkipTest("Missing one or more installed: 'hdf2gif', 'gif2hdf'")

        gif_fn = f"{base_name}.gif"
        new_hdf_fn = f"{base_name}gif.hdf"

        with test_part(
            self, "test_gif_converters_hdf2gif", purpose=f"convert {base_name} hdf-to-gif"
        ):
            hdf2gif = which(self.prefix.bin.hdf2gif)
            hdf2gif(storm_fn, gif_fn)

        with test_part(
            self, "test_gif_converters_gif2hdf", purpose=f"convert {base_name} gif-to-hdf"
        ):
            gif2hdf = which(self.prefix.bin.gif2hdf)
            gif2hdf(gif_fn, new_hdf_fn)

        with test_part(
            self, "test_gif_converters_hdiff", purpose=f"compare new and orig {base_name} hdf"
        ):
            hdiff = which(self.prefix.bin.hdiff)
            hdiff(new_hdf_fn, storm_fn)

    def test_list(self):
        """compare low-level HDF file information to expected"""
        base_name = "storm110"
        if not os.path.isfile(self.prefix.bin.hdfls):
            raise SkipTest("hdfls is not installed")

        test_data_dir = self.test_suite.current_test_data_dir
        details_file = os.path.join(test_data_dir, f"{base_name}.out")
        expected = get_escaped_text_output(details_file)

        storm_fn = os.path.join(self.cached_tests_work_dir, f"{base_name}.hdf")

        hdfls = which(self.prefix.bin.hdfls)
        out = hdfls(storm_fn, output=str.split, error=str.split)
        check_outputs(expected, out)

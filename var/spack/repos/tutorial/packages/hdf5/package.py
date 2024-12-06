# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

import llnl.util.tty as tty

from spack.package import *


class Hdf5(CMakePackage):
    """HDF5 is a data model, library, and file format for storing and managing
    data. It supports an unlimited variety of datatypes, and is designed for
    flexible and efficient I/O and for high volume and complex data.
    """

    homepage = "https://portal.hdfgroup.org"
    url = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.7/src/hdf5-1.10.7.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/HDF5/releases"
    list_depth = 3
    git = "https://github.com/HDFGroup/hdf5.git"
    maintainers(
        "lrknox",
        "brtnfld",
        "byrnHDF",
        "ChristopherHogan",
        "epourmal",
        "gheber",
        "hyoklee",
        "lkurz",
        "soumagne",
    )

    test_requires_compiler = True

    # The 'develop' version is renamed so that we could uninstall (or patch) it
    # without affecting other develop version.
    version("develop-1.13", branch="develop")
    version("develop-1.12", branch="hdf5_1_12")
    version("develop-1.10", branch="hdf5_1_10")
    version("develop-1.8", branch="hdf5_1_8")

    version("1.12.1", sha256="79c66ff67e666665369396e9c90b32e238e501f345afd2234186bfb8331081ca")
    version("1.12.0", sha256="a62dcb276658cb78e6795dd29bf926ed7a9bc4edf6e77025cd2c689a8f97c17a")
    # HDF5 1.12 broke API compatibility, so we currently prefer the latest
    # 1.10 release.  packages that want later versions of HDF5 should specify,
    # e.g., depends_on("hdf5@1.12:") to get 1.12 or higher.
    version(
        "1.10.7",
        sha256="7a1a0a54371275ce2dfc5cd093775bb025c365846512961e7e5ceaecb437ef15",
        preferred=True,
    )
    version("1.10.6", sha256="5f9a3ee85db4ea1d3b1fa9159352aebc2af72732fc2f58c96a3f0768dba0e9aa")
    version("1.10.5", sha256="6d4ce8bf902a97b050f6f491f4268634e252a63dadd6656a1a9be5b7b7726fa8")
    version("1.10.4", sha256="8f60dc4dd6ab5fcd23c750d1dc5bca3d0453bdce5c8cdaf0a4a61a9d1122adb2")
    version("1.10.3", sha256="b600d7c914cfa80ae127cd1a1539981213fee9994ac22ebec9e3845e951d9b39")
    version("1.10.2", sha256="bfec1be8c366965a99812cf02ddc97e4b708c1754fccba5414d4adccdc073866")
    version("1.10.1", sha256="048a9d149fb99aaa1680a712963f5a78e9c43b588d0e79d55e06760ec377c172")
    version(
        "1.10.0-patch1", sha256="6e78cfe32a10e6e0629393cdfddf6cfa536571efdaf85f08e35326e1b4e9eff0"
    )
    version("1.10.0", sha256="81f6201aba5c30dced5dcd62f5d5477a2790fd5850e02ac514ca8bf3e2bb375a")

    version("1.8.22", sha256="8406d96d9355ef8961d2739fb8fd5474ad4cdf52f3cfac657733defd9709bfaa")
    version("1.8.21", sha256="87d8c82eba5cf766d97cd06c054f4639c1049c4adeaa3a79f77f8bd374f80f37")
    version("1.8.19", sha256="a4335849f19fae88c264fd0df046bc321a78c536b2548fc508627a790564dc38")
    version("1.8.18", sha256="cdb195ad8d9e6782acf24b2488061289f615628c2ccda8457b0a0c3fb7a8a063")
    version("1.8.17", sha256="d9cda297ee76ade9881c4208987939250d397bae6252d0ccb66fa7d24d67e263")
    version("1.8.16", sha256="ed17178abd9928a7237f30370189ba767b9e39e0db45917c2ac4665eb9cb4771")
    version("1.8.15", sha256="4e963216b7d32469596bc1321a8c3f6e0c278dcbbdb7be6414c63c081b34c275")
    version("1.8.14", sha256="1dbefeeef7f591897c632b2b090db96bb8d35ad035beaa36bc39cb2bc67e0639")
    version("1.8.13", sha256="82f6b38eec103b4fccfbf14892786e0c27a8135d3252d8601cf5bf20066d38c1")
    version("1.8.12", sha256="b5cccea850096962b5fd9e96f22c4f47d2379224bb41130d9bc038bb6c37dfcb")
    version("1.8.10", sha256="4813b79c5fb8701a625b9924b8203bc7154a77f9b826ad4e034144b4056a160a")

    variant("shared", default=True, description="Builds a shared version of the library")

    variant("hl", default=False, description="Enable the high-level library")
    variant("cxx", default=False, description="Enable C++ support")
    variant("fortran", default=False, description="Enable Fortran support")
    variant("java", default=False, description="Enable Java support")
    variant("threadsafe", default=False, description="Enable thread-safe capabilities")
    variant("tools", default=True, description="Enable building tools")
    variant("mpi", default=True, description="Enable MPI support")
    variant("szip", default=False, description="Enable szip support")
    # Build HDF5 with API compatibility.
    variant(
        "api",
        default="default",
        description="Choose api compatibility for earlier version",
        values=("default", "v114", "v112", "v110", "v18", "v16"),
        multi=False,
    )

    depends_on("cmake@3.12:", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("java", type=("build", "run"), when="+java")
    # numactl does not currently build on darwin
    if sys.platform != "darwin":
        depends_on("numactl", when="+mpi+fortran")
    depends_on("szip", when="+szip")
    depends_on("zlib-api")

    # The compiler wrappers (h5cc, h5fc, etc.) run 'pkg-config'.
    depends_on("pkgconfig", type="run")

    conflicts("api=v114", when="@1.6.0:1.12", msg="v114 is not compatible with this release")
    conflicts("api=v112", when="@1.6.0:1.10", msg="v112 is not compatible with this release")
    conflicts("api=v110", when="@1.6.0:1.8", msg="v110 is not compatible with this release")
    conflicts("api=v18", when="@1.6.0:1.6", msg="v18 is not compatible with this release")

    # The Java wrappers and associated libhdf5_java library
    # were first available in 1.10
    conflicts("+java", when="@:1.9")
    # The Java wrappers cannot be built without shared libs.
    conflicts("+java", when="~shared")

    # There are several officially unsupported combinations of the features:
    # 1. Thread safety is not guaranteed via high-level C-API but in some cases
    #    it works.
    # conflicts('+threadsafe+hl')

    # 2. Thread safety is not guaranteed via Fortran (CXX) API, but it's
    #    possible for a dependency tree to contain a package that uses Fortran
    #    (CXX) API in a single thread and another one that uses low-level C-API
    #    in multiple threads. To allow for such scenarios, we don't specify the
    #    following conflicts.
    # conflicts('+threadsafe+cxx')
    # conflicts('+threadsafe+fortran')

    # 3. Parallel features are not supported via CXX API, but for the reasons
    #    described in #2 we allow for such combination.
    # conflicts('+mpi+cxx')

    # There are known build failures with intel@18.0.1. This issue is
    # discussed and patch is provided at
    # https://software.intel.com/en-us/forums/intel-fortran-compiler-for-linux-and-mac-os-x/topic/747951.
    patch("h5f90global-mult-obj-same-equivalence-same-common-block.patch", when="@1.10.1%intel@18")

    # Turn line comments into block comments to conform with pre-C99 language
    # standards. Versions of hdf5 after 1.8.10 don't require this patch,
    # either because they conform to pre-C99 or neglect to ask for pre-C99
    # language standards from their compiler. The hdf5 build system adds
    # the -ansi cflag (run 'man gcc' for info on -ansi) for some versions
    # of some compilers (see hdf5-1.8.10/config/gnu-flags). The hdf5 build
    # system does not provide an option to disable -ansi, but since the
    # pre-C99 code is restricted to just five lines of line comments in
    # three src files, this patch accomplishes the simple task of patching the
    # three src files and leaves the hdf5 build system alone.
    patch("pre-c99-comments.patch", when="@1.8.10")

    # There are build errors with GCC 8, see
    # https://forum.hdfgroup.org/t/1-10-2-h5detect-compile-error-gcc-8-1-0-on-centos-7-2-solved/4441
    patch(
        "https://salsa.debian.org/debian-gis-team/hdf5/raw/bf94804af5f80f662cad80a5527535b3c6537df6/debian/patches/gcc-8.patch",
        sha256="57cee5ff1992b4098eda079815c36fc2da9b10e00a9056df054f2384c4fc7523",
        when="@1.10.2%gcc@8:",
    )

    # Disable MPI C++ interface when C++ is disabled, otherwise downstream
    # libraries fail to link; see https://github.com/spack/spack/issues/12586
    patch(
        "h5public-skip-mpicxx.patch",
        when="@1.8.10:1.8.21,1.10.0:1.10.5+mpi~cxx",
        sha256="b61e2f058964ad85be6ee5ecea10080bf79e73f83ff88d1fa4b602d00209da9c",
    )

    # Fixes BOZ literal constant error when compiled with GCC 10.
    # The issue is described here: https://github.com/spack/spack/issues/18625
    patch(
        "hdf5_1.8_gcc10.patch",
        when="@:1.8.21",
        sha256="0e20187cda3980a4fdff410da92358b63de7ebef2df1d7a425371af78e50f666",
    )

    # The argument 'buf_size' of the C function 'h5fget_file_image_c' is
    # declared as intent(in) though it is modified by the invocation. As a
    # result, aggressive compilers such as Fujitsu's may do a wrong
    # optimization to cause an error.
    def patch(self):
        filter_file(
            "INTEGER(SIZE_T), INTENT(IN) :: buf_size",
            "INTEGER(SIZE_T), INTENT(OUT) :: buf_size",
            "fortran/src/H5Fff.F90",
            string=True,
            ignore_absent=True,
        )
        filter_file(
            "INTEGER(SIZE_T), INTENT(IN) :: buf_size",
            "INTEGER(SIZE_T), INTENT(OUT) :: buf_size",
            "fortran/src/H5Fff_F03.f90",
            string=True,
            ignore_absent=True,
        )

    # The parallel compiler wrappers (i.e. h5pcc, h5pfc, etc.) reference MPI
    # compiler wrappers and do not need to be changed.
    filter_compiler_wrappers(
        "h5cc", "h5hlcc", "h5fc", "h5hlfc", "h5c++", "h5hlc++", relative_root="bin"
    )

    def url_for_version(self, version):
        url = (
            "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-{0}/hdf5-{1}/src/hdf5-{1}.tar.gz"
        )
        return url.format(version.up_to(2), version)

    def flag_handler(self, name, flags):
        cmake_flags = []

        if name == "cflags":
            if self.spec.satisfies("%gcc") or self.spec.satisfies("%clang"):
                # Quiet warnings/errors about implicit declaration of functions
                # in C99:
                cmake_flags.append("-Wno-implicit-function-declaration")
                # Note that this flag will cause an error if building %nvhpc.
            if self.spec.satisfies("@:1.8.12~shared"):
                # More recent versions set CMAKE_POSITION_INDEPENDENT_CODE to
                # True and build with PIC flags.
                cmake_flags.append(self.compiler.cc_pic_flag)
        elif name == "cxxflags":
            if self.spec.satisfies("@:1.8.12+cxx~shared"):
                cmake_flags.append(self.compiler.cxx_pic_flag)
        elif name == "fflags":
            if self.spec.satisfies("@:1.8.12+fortran~shared"):
                cmake_flags.append(self.compiler.fc_pic_flag)
        elif name == "ldlibs":
            if "+fortran %fj" in self.spec:
                cmake_flags.extend(["-lfj90i", "-lfj90f", "-lfjsrcinfo", "-lelf"])

        return flags, None, (cmake_flags or None)

    @property
    def libs(self):
        """HDF5 can be queried for the following parameters:

        - "hl": high-level interface
        - "cxx": C++ APIs
        - "fortran": Fortran APIs
        - "java": Java APIs

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        shared = "+shared" in self.spec

        # This map contains a translation from query_parameters
        # to the libraries needed
        query2libraries = {
            tuple(): ["libhdf5"],
            ("cxx", "fortran", "hl", "java"): [
                # When installed with Autotools, the basename of the real
                # library file implementing the High-level Fortran interface is
                # 'libhdf5hl_fortran'. Starting versions 1.8.22, 1.10.5 and
                # 1.12.0, the Autotools installation also produces a symbolic
                # link 'libhdf5_hl_fortran.<so/a>' to
                # 'libhdf5hl_fortran.<so/a>'. Note that in the case of the
                # dynamic library, the latter is a symlink to the real sonamed
                # file 'libhdf5_fortran.so.<abi-version>'. This means that all
                # dynamically linked executables/libraries of the dependent
                # packages need 'libhdf5_fortran.so.<abi-version>' with the same
                # DT_SONAME entry. However, the CMake installation (at least
                # starting version 1.8.10) does not produce it. Instead, the
                # basename of the library file is 'libhdf5_hl_fortran'. Which
                # means that switching to CMake requires rebuilding of all
                # dependant packages that use the High-level Fortran interface.
                # Therefore, we do not try to preserve backward compatibility
                # with Autotools installations by creating symlinks. The only
                # packages that could benefit from it would be those that
                # hardcode the library name in their building systems. Such
                # packages should simply be patched.
                "libhdf5_hl_fortran",
                "libhdf5_hl_f90cstub",
                "libhdf5_hl_cpp",
                "libhdf5_hl",
                "libhdf5_fortran",
                "libhdf5_f90cstub",
                "libhdf5_java",
                "libhdf5",
            ],
            ("cxx", "hl"): ["libhdf5_hl_cpp", "libhdf5_hl", "libhdf5"],
            ("fortran", "hl"): [
                "libhdf5_hl_fortran",
                "libhdf5_hl_f90cstub",
                "libhdf5_hl",
                "libhdf5_fortran",
                "libhdf5_f90cstub",
                "libhdf5",
            ],
            ("hl",): ["libhdf5_hl", "libhdf5"],
            ("cxx", "fortran"): ["libhdf5_fortran", "libhdf5_f90cstub", "libhdf5_cpp", "libhdf5"],
            ("cxx",): ["libhdf5_cpp", "libhdf5"],
            ("fortran",): ["libhdf5_fortran", "libhdf5_f90cstub", "libhdf5"],
            ("java",): ["libhdf5_java", "libhdf5"],
        }

        # Turn the query into the appropriate key
        key = tuple(sorted(query_parameters))
        libraries = query2libraries[key]

        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

    @when("@:1.8.21,1.10.0:1.10.5+szip")
    def setup_build_environment(self, env):
        env.set("SZIP_INSTALL", self.spec["szip"].prefix)

    @run_before("cmake")
    def fortran_check(self):
        if "+fortran" in self.spec and not self.compiler.fc:
            msg = "cannot build a Fortran variant without a Fortran compiler"
            raise RuntimeError(msg)

    def cmake_args(self):
        spec = self.spec

        if spec.satisfies("@:1.8.15+shared"):
            tty.warn("hdf5@:1.8.15+shared does not produce static libraries")

        args = [
            # Always enable this option. This does not actually enable any
            # features: it only *allows* the user to specify certain
            # combinations of other arguments.
            self.define("ALLOW_UNSUPPORTED", True),
            # Speed-up the building by skipping the examples:
            self.define("HDF5_BUILD_EXAMPLES", False),
            self.define(
                "BUILD_TESTING",
                self.run_tests or
                # Version 1.8.22 fails to build the tools when shared libraries
                # are enabled but the tests are disabled.
                spec.satisfies("@1.8.22+shared+tools"),
            ),
            self.define("HDF5_ENABLE_Z_LIB_SUPPORT", True),
            self.define_from_variant("HDF5_ENABLE_SZIP_SUPPORT", "szip"),
            self.define_from_variant("HDF5_ENABLE_SZIP_ENCODING", "szip"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("ONLY_SHARED_LIBS", False),
            self.define_from_variant("HDF5_ENABLE_PARALLEL", "mpi"),
            self.define_from_variant("HDF5_ENABLE_THREADSAFE", "threadsafe"),
            self.define_from_variant("HDF5_BUILD_HL_LIB", "hl"),
            self.define_from_variant("HDF5_BUILD_CPP_LIB", "cxx"),
            self.define_from_variant("HDF5_BUILD_FORTRAN", "fortran"),
            self.define_from_variant("HDF5_BUILD_JAVA", "java"),
            self.define_from_variant("HDF5_BUILD_TOOLS", "tools"),
        ]

        api = spec.variants["api"].value
        if api != "default":
            args.append(self.define("DEFAULT_API_VERSION", api))

        if "+mpi" in spec:
            args.append(self.define("CMAKE_C_COMPILER", spec["mpi"].mpicc))

            if "+cxx" in self.spec:
                args.append(self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx))

            if "+fortran" in self.spec:
                args.append(self.define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc))

        return args

    @run_after("install")
    def ensure_parallel_compiler_wrappers(self):
        # When installed with Autotools and starting at least version 1.8.10,
        # the package produces C compiler wrapper called either 'h5cc' (when MPI
        # support is disabled) or 'h5pcc' (when MPI support is enabled). The
        # CMake installation produces the wrapper called 'h5cc' (regardless of
        # whether MPI support is enabled) only starting versions 1.8.21, 1.10.2
        # and 1.12.0. The current develop versions also produce 'h5pcc' when MPI
        # support is enabled and the file is identical to 'h5cc'. Here, we make
        # sure that 'h5pcc' is available when MPI support is enabled (only for
        # versions that generate 'h5cc').
        if self.spec.satisfies("@1.8.21:1.8.22,1.10.2:1.10.7,1.12.0+mpi"):
            with working_dir(self.prefix.bin):
                # No try/except here, fix the condition above instead:
                symlink("h5cc", "h5pcc")

        # The same as for 'h5pcc'. However, the CMake installation produces the
        # Fortran compiler wrapper called 'h5fc' only starting versions 1.8.22,
        # 1.10.6 and 1.12.0. The current develop versions do not produce 'h5pfc'
        # at all. Here, we make sure that 'h5pfc' is available when Fortran and
        # MPI support are enabled (only for versions that generate 'h5fc').
        if self.spec.satisfies(
            "@1.8.22:1.8," "1.10.6:1.10," "1.12.0:1.12," "develop:" "+fortran+mpi"
        ):
            with working_dir(self.prefix.bin):
                # No try/except here, fix the condition above instead:
                symlink("h5fc", "h5pfc")

    @run_after("install")
    def fix_package_config(self):
        # We need to fix the pkg-config files, which are also used by the
        # compiler wrappers. The files are created starting versions 1.8.21,
        # 1.10.2 and 1.12.0. However, they are broken (except for the version
        # 1.8.22): the files are named <name>-<version>.pc but reference <name>
        # packages. This was fixed in the develop versions at some point: the
        # files started referencing <name>-<version> packages but got broken
        # again: the files got names <name>.pc but references had not been
        # updated accordingly. Another issue, which we address here, is that
        # some Linux distributions install pkg-config files named hdf5.pc and we
        # want to override them. Therefore, the following solution makes sure
        # that each <name>-<version>.pc file is symlinked by <name>.pc and all
        # references to <name>-<version> packages in the original files are
        # replaced with references to <name> packages.
        pc_files = find(self.prefix.lib.pkgconfig, "hdf5*.pc", recursive=False)

        if not pc_files:
            # This also tells us that the pkgconfig directory does not exist.
            return

        # Replace versioned references in all pkg-config files:
        filter_file(
            r"(Requires(?:\.private)?:.*)(hdf5[^\s,]*)(?:-[^\s,]*)(.*)",
            r"\1\2\3",
            *pc_files,
            backup=False,
        )

        # Create non-versioned symlinks to the versioned pkg-config files:
        with working_dir(self.prefix.lib.pkgconfig):
            for f in pc_files:
                src_filename = os.path.basename(f)
                version_sep_idx = src_filename.find("-")
                if version_sep_idx > -1:
                    tgt_filename = src_filename[:version_sep_idx] + ".pc"
                    if not os.path.exists(tgt_filename):
                        symlink(src_filename, tgt_filename)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        self._check_install()

    def _check_install(self):
        # Build and run a small program to test the installed HDF5 library
        spec = self.spec
        print("Checking HDF5 installation...")
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""
#include <hdf5.h>
#include <assert.h>
#include <stdio.h>
int main(int argc, char **argv) {
  unsigned majnum, minnum, relnum;
  herr_t herr = H5get_libversion(&majnum, &minnum, &relnum);
  assert(!herr);
  printf("HDF5 version %d.%d.%d %u.%u.%u\n", H5_VERS_MAJOR, H5_VERS_MINOR,
         H5_VERS_RELEASE, majnum, minnum, relnum);
  return 0;
}
"""
            expected = """\
HDF5 version {version} {version}
""".format(
                version=str(spec.version.up_to(3))
            )
            with open("check.c", "w") as f:
                f.write(source)
            if "+mpi" in spec:
                cc = Executable(spec["mpi"].mpicc)
            else:
                cc = Executable(self.compiler.cc)
            cc(*(["-c", "check.c"] + spec["hdf5"].headers.cpp_flags.split()))
            cc(*(["-o", "check", "check.o"] + spec["hdf5"].libs.ld_flags.split()))
            try:
                check = Executable("./check")
                output = check(output=str)
            except ProcessError:
                output = ""
            success = output == expected
            if not success:
                print("Produced output does not match expected output.")
                print("Expected output:")
                print("-" * 80)
                print(expected)
                print("-" * 80)
                print("Produced output:")
                print("-" * 80)
                print(output)
                print("-" * 80)
                raise RuntimeError("HDF5 install check failed")
        shutil.rmtree(checkdir)

    def _test_check_versions(self):
        """Perform version checks on selected installed package binaries."""
        spec_vers_str = "Version {0}".format(self.spec.version)

        exes = [
            "h5copy",
            "h5diff",
            "h5dump",
            "h5format_convert",
            "h5ls",
            "h5mkgrp",
            "h5repack",
            "h5stat",
            "h5unjam",
        ]
        use_short_opt = ["h52gif", "h5repart", "h5unjam"]
        for exe in exes:
            reason = "test: ensuring version of {0} is {1}".format(exe, spec_vers_str)
            option = "-V" if exe in use_short_opt else "--version"
            self.run_test(
                exe, option, spec_vers_str, installed=True, purpose=reason, skip_missing=True
            )

    def _test_example(self):
        """This test performs copy, dump, and diff on an example hdf5 file."""
        test_data_dir = self.test_suite.current_test_data_dir

        filename = "spack.h5"
        h5_file = test_data_dir.join(filename)

        reason = "test: ensuring h5dump produces expected output"
        expected = get_escaped_text_output(test_data_dir.join("dump.out"))
        self.run_test(
            "h5dump",
            filename,
            expected,
            installed=True,
            purpose=reason,
            skip_missing=True,
            work_dir=test_data_dir,
        )

        reason = "test: ensuring h5copy runs"
        options = ["-i", h5_file, "-s", "Spack", "-o", "test.h5", "-d", "Spack"]
        self.run_test(
            "h5copy", options, [], installed=True, purpose=reason, skip_missing=True, work_dir="."
        )

        reason = "test: ensuring h5diff shows no differences between orig and" " copy"
        self.run_test(
            "h5diff",
            [h5_file, "test.h5"],
            [],
            installed=True,
            purpose=reason,
            skip_missing=True,
            work_dir=".",
        )

    def test(self):
        """Perform smoke tests on the installed package."""
        # Simple version check tests on known binaries
        self._test_check_versions()

        # Run sequence of commands on an hdf5 file
        self._test_example()

        # Run existing install check
        self._check_install()

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *


class ParallelNetcdf(AutotoolsPackage):
    """PnetCDF (Parallel netCDF) is a high-performance parallel I/O
    library for accessing files in format compatibility with Unidata's
    NetCDF, specifically the formats of CDF-1, 2, and 5.
    """

    homepage = "https://parallel-netcdf.github.io/"
    git = "https://github.com/Parallel-NetCDF/PnetCDF"
    url = "https://parallel-netcdf.github.io/Release/pnetcdf-1.11.0.tar.gz"
    list_url = "https://parallel-netcdf.github.io/wiki/Download.html"

    maintainers("skosukhin")

    tags = ["e4s"]

    test_requires_compiler = True

    def url_for_version(self, version):
        if version >= Version("1.11.0"):
            url = f"https://parallel-netcdf.github.io/Release/pnetcdf-{version.dotted}.tar.gz"
        else:
            url = f"https://parallel-netcdf.github.io/Release/parallel-netcdf-{version.dotted}.tar.gz"

        return url

    version("master", branch="master")
    version("1.12.3", sha256="439e359d09bb93d0e58a6e3f928f39c2eae965b6c97f64e67cd42220d6034f77")
    version("1.12.2", sha256="3ef1411875b07955f519a5b03278c31e566976357ddfc74c2493a1076e7d7c74")
    version("1.12.1", sha256="56f5afaa0ddc256791c405719b6436a83b92dcd5be37fe860dea103aee8250a2")
    version("1.11.2", sha256="d2c18601b364c35b5acb0a0b46cd6e14cae456e0eb854e5c789cf65f3cd6a2a7")
    version("1.11.1", sha256="0c587b707835255126a23c104c66c9614be174843b85b897b3772a590be45779")
    version("1.11.0", sha256="a18a1a43e6c4fd7ef5827dbe90e9dcf1363b758f513af1f1356ed6c651195a9f")
    version("1.10.0", sha256="ed189228b933cfeac3b7b4f8944eb00e4ff2b72cf143365b1a77890980663a09")
    version("1.9.0", sha256="356e1e1fae14bc6c4236ec11435cfea0ff6bde2591531a4a329f9508a01fbe98")
    version("1.8.1", sha256="8d7d4c9c7b39bb1cbbcf087e0d726551c50f0cc30d44aed3df63daf3772c9043")
    version("1.8.0", sha256="ac00bb2333bee96354de9d9c32d3dfdaa919d878098762f146996578b7f0ede9")
    version("1.7.0", sha256="52f0d106c470a843c6176318141f74a21e6ece3f70ee8fe261c6b93e35f70a94")
    version("1.6.1", sha256="8cf1af7b640475e3cc931e5fbcfe52484c5055f2fab526691933c02eda388aae")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("cxx", default=True, description="Build the C++ Interface")
    variant("fortran", default=True, description="Build the Fortran Interface")
    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("shared", default=True, description="Enable shared library")
    variant("burstbuffer", default=False, description="Enable burst buffer feature")

    depends_on("mpi")

    depends_on("m4", type="build")
    depends_on("autoconf", when="@master", type="build")
    depends_on("automake", when="@master", type="build")
    depends_on("libtool", when="@master", type="build")

    depends_on("perl", type="build")

    # Suport for shared libraries was introduced in version 1.9.0
    conflicts("+shared", when="@:1.8")
    conflicts("+burstbuffer", when="@:1.10")

    # Before 1.10.0, C utility programs (e.g. ncmpigen) were linked without
    # explicit specification of the Fortran runtime libraries, which is
    # required when libpnetcdf.so contains Fortran symbols. Libtool sets the
    # required linking flags implicitly but only if the Fortran compiler
    # produces verbose output with the '-v' flag (and, due to a bug in Libtool,
    # when CXX is not set to 'no'; see macro _LT_LANG_FC_CONFIG in libtool.m4
    # for more details). The latter is not the case for NAG. Starting 1.10.0,
    # the required linking flags are explicitly set in the makefiles and
    # detected using macro AC_FC_LIBRARY_LDFLAGS, which means that we can
    # override the verbose output flag for Fortran compiler on the command line
    # (see below).
    conflicts("+shared", when="@:1.9%nag+fortran")

    @property
    def libs(self):
        libraries = ["libpnetcdf"]

        query_parameters = self.spec.last_query.extra_parameters

        if "shared" in query_parameters:
            shared = True
        elif "static" in query_parameters:
            shared = False
        else:
            shared = "+shared" in self.spec

        libs = find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

        if libs:
            return libs

        msg = f"Unable to recursively locate {'shared' if shared else 'static'} \
{self.spec.name} libraries in {self.spec.prefix}"
        raise spack.error.NoLibrariesError(msg)

    @when("@master")
    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            # We do not specify '-f' because we need to use libtool files from
            # the repository.
            autoreconf("-iv")

    def configure_args(self):
        args = ["--with-mpi=%s" % self.spec["mpi"].prefix, "SEQ_CC=%s" % spack_cc]

        args += self.enable_or_disable("cxx")
        args += self.enable_or_disable("fortran")

        flags = {"CFLAGS": [], "CXXFLAGS": [], "FFLAGS": [], "FCFLAGS": []}

        if "+pic" in self.spec:
            flags["CFLAGS"].append(self.compiler.cc_pic_flag)
            flags["CXXFLAGS"].append(self.compiler.cxx_pic_flag)
            flags["FFLAGS"].append(self.compiler.f77_pic_flag)
            flags["FCFLAGS"].append(self.compiler.fc_pic_flag)

        # https://github.com/Parallel-NetCDF/PnetCDF/issues/61
        if self.spec.satisfies("%gcc@10:"):
            flags["FFLAGS"].append("-fallow-argument-mismatch")
            flags["FCFLAGS"].append("-fallow-argument-mismatch")

        for key, value in sorted(flags.items()):
            if value:
                args.append(f"{key}={' '.join(value)}")

        if self.version >= Version("1.8"):
            args.append("--enable-relax-coord-bound")

        if self.version >= Version("1.9"):
            args += self.enable_or_disable("shared")
            args.extend(["--enable-static", "--disable-silent-rules"])

        if self.spec.satisfies("%nag+fortran+shared"):
            args.extend(["ac_cv_prog_fc_v=-Wl,-v", "ac_cv_prog_f77_v=-Wl,-v"])

        if "+burstbuffer" in self.spec:
            args.append("--enable-burst-buffering")

        return args

    examples_src_dir = join_path("examples", "CXX")

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.examples_src_dir])

    def test_column_wise(self):
        """build and run column_wise"""
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)
        # pnetcdf has many examples to serve as a suitable smoke check.
        # column_wise was chosen based on the E4S test suite. Other
        # examples should work as well.
        test_exe = "column_wise"
        options = [
            f"{test_exe}.cpp",
            "-o",
            test_exe,
            "-lpnetcdf",
            f"-L{self.prefix.lib}",
            f"-I{self.prefix.include}",
        ]

        with working_dir(test_dir):
            mpicxx = which(self.spec["mpi"].prefix.bin.mpicxx)
            mpicxx(*options)

            mpiexe_list = [
                "srun",
                self.spec["mpi"].prefix.bin.mpirun,
                self.spec["mpi"].prefix.bin.mpiexec,
            ]

            for mpiexe in mpiexe_list:
                tty.info(f"Attempting to build and launch with {os.path.basename(mpiexe)}")
                try:
                    args = ["--immediate=30"] if mpiexe == "srun" else []
                    args += ["-n", "1", test_exe]
                    exe = which(mpiexe)
                    exe(*args)
                    rm = which("rm")
                    rm("-f", "column_wise")
                    return

                except (Exception, ProcessError) as err:
                    tty.info(f"Skipping {mpiexe}: {str(err)}")

        assert False, "No MPI executable was found"

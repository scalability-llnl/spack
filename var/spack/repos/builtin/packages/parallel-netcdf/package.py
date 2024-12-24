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
    with default_args(deprecated=True):
        version(
            "1.12.2", sha256="3ef1411875b07955f519a5b03278c31e566976357ddfc74c2493a1076e7d7c74"
        )
        version(
            "1.12.1", sha256="56f5afaa0ddc256791c405719b6436a83b92dcd5be37fe860dea103aee8250a2"
        )
        version(
            "1.11.2", sha256="d2c18601b364c35b5acb0a0b46cd6e14cae456e0eb854e5c789cf65f3cd6a2a7"
        )
        version(
            "1.11.1", sha256="0c587b707835255126a23c104c66c9614be174843b85b897b3772a590be45779"
        )
        version(
            "1.11.0", sha256="a18a1a43e6c4fd7ef5827dbe90e9dcf1363b758f513af1f1356ed6c651195a9f"
        )

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

    # Link to issue here
    patch("parallel-netcdf-1.12.3-intel-irc-intlc.patch", when="@1.12.3 %intel")
    patch("parallel-netcdf-1.12.3-intel-irc-intlc.patch", when="@1.12.3 %oneapi")

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
        if self.spec["mpi"].satisfies("intel-oneapi-mpi"):
            prefix = os.path.join(self.spec["mpi"].prefix, "mpi", str(self.spec["mpi"].version))
        else:
            prefix = self.spec["mpi"].prefix
        args = ["--with-mpi=%s" % prefix, "SEQ_CC=%s" % spack_cc]

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

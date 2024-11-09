# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import tempfile

from spack.package import *


class Wps(Package):
    """The Weather Research and Forecasting Pre-Processing System (WPS)"""

    homepage = "https://www.mmm.ucar.edu/weather-research-and-forecasting-model"
    url = "https://github.com/wrf-model/WPS/archive/v4.2.tar.gz"
    maintainers("MichaelLaufer")

    version("4.5", sha256="3cb29107f85b81af05b7dd494e5d4a13cf1b33b87d7e2911a64a7abc59bf55f3")
    version("4.4", sha256="fe9c8d8a9a4abbf800b30e6cbb378604c6040e4536f5594b8e2dae43e942e2b3")
    version("4.3.1", sha256="db6da44a2ca68cc289e98ab388a53c27283eb4ed8e92edee268466543fdedb0e")
    version("4.3", sha256="1913cb24de549f029d65635feea27f3304a8f42ec025954a0887651fc89d1e9e")
    version("4.2", sha256="3e175d033355d3e7638be75bc7c0bc0de6da299ebd175a9bbc1b7a121acd0168")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Serial variant recommended in WRF/WPS docs
    variant(
        "build_type",
        default="serial",
        description="Build type",
        values=("serial", "serial_NO_GRIB2", "dmpar", "dmpar_NO_GRIB2"),
    )

    # These patches deal with netcdf & netcdf-fortran being two diff things
    patch("patches/4.2/arch.Config.pl.patch", when="@4.2:")
    patch("patches/4.2/arch.configure.defaults.patch", when="@4.2")
    patch("patches/4.2/configure.patch", when="@4.2:4.3.1")
    patch("patches/4.2/preamble.patch", when="@4.2:")
    patch("patches/4.3/arch.configure.defaults.patch", when="@=4.3")
    patch("patches/4.3.1/arch.configure.defaults.patch", when="@4.3.1")
    patch("patches/4.4/configure.patch", when="@4.4:")

    # According to:
    # http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.0/users_guide_chap2.html#_Required_Compilers_and_1
    # Section: "Required/Optional Libraries to Download"
    depends_on("wrf")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("mpi")
    # build script use csh
    depends_on("tcsh", type=("build"))

    # this fixes that for csh install scripts
    depends_on("time", type=("build"))
    depends_on("m4", type="build")
    depends_on("libtool", type="build")
    depends_on("jasper@:2")
    phases = ["configure", "build", "install"]

    patch("for_aarch64.patch", when="target=aarch64:")

    def setup_build_environment(self, env):
        env.set("WRF_DIR", self.spec["wrf"].prefix)
        env.set("NETCDF", self.spec["netcdf-c"].prefix)
        # This gets used via the applied patch files
        env.set("NETCDFF", self.spec["netcdf-fortran"].prefix)
        env.set("JASPERINC", self.spec["jasper"].prefix.include)
        env.set("JASPERLIB", self.spec["jasper"].prefix.lib)

        if self.spec.satisfies("%gcc@10:"):
            args = "-w -O2 -fallow-argument-mismatch -fallow-invalid-boz"
            env.set("FCFLAGS", args)
            env.set("FFLAGS", args)

    def setup_run_environment(self, env):
        env.append_path("PATH", self.prefix)
        env.append_path("PATH", self.prefix.util)

    def patch(self):
        # Let's not assume csh is intalled in bin
        files = glob.glob("*.csh")

        filter_file("^#!/bin/csh -f", "#!/usr/bin/env csh", *files)
        filter_file("^#!/bin/csh", "#!/usr/bin/env csh", *files)

    def configure(self, spec, prefix):
        build_opts = {
            "gcc": {"serial": "1", "serial_NO_GRIB2": "2", "dmpar": "3", "dmpar_NO_GRIB2": "4"},
            "intel": {
                "serial": "17",
                "serial_NO_GRIB2": "18",
                "dmpar": "19",
                "dmpar_NO_GRIB2": "20",
            },
            "pgi": {"serial": "5", "serial_NO_GRIB2": "6", "dmpar": "7", "dmpar_NO_GRIB2": "8"},
        }

        try:
            compiler_opts = build_opts[self.spec.compiler.name]
        except KeyError:
            raise InstallError("Compiler not recognized nor supported.")

        # Spack already makes sure that the variant value is part of the set.
        build_type = compiler_opts[spec.variants["build_type"].value]

        with tempfile.TemporaryFile(mode="w") as fp:
            fp.write(build_type + "\n")
            fp.seek(0)
            Executable("./configure")(input=fp)

    def build(self, spec, prefix):
        csh = which("csh")
        csh("./compile")

    def install(self, spec, prefix):
        # Copy all of WPS staging dir to install dir
        install_tree(".", prefix)

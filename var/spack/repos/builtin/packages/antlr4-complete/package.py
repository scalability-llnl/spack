# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Antlr4Complete(Package):
    """
    This package provides complete ANTLR tool, Java runtime and ST,
    which lets you run the tool and the generated code by
    version 4 of ANTLR (ANother Tool for Language Recognition).
    """

    homepage = "https://www.antlr.org"
    url = "https://www.antlr.org/download/antlr-4.13.1-complete.jar"

    version(
        "4.13.1",
        sha256="bc13a9c57a8dd7d5196888211e5ede657cb64a3ce968608697e4f668251a8487",
        expand=False,
    )
    version(
        "4.12.0",
        sha256="88f18a2bfac0dde1009eda5c7dce358a52877faef7868f56223a5bcc15329e43",
        expand=False,
    )
    version(
        "4.11.1",
        sha256="62975e192b4af2622b72b5f0131553ee3cbce97f76dc2a41632dcc55e25473e1",
        expand=False,
    )
    version(
        "4.10.1",
        sha256="41949d41f20d31d5b8277187735dd755108df52b38db6c865108d3382040f918",
        expand=False,
    )
    version(
        "4.9.3",
        sha256="afcd40946d3de4d81e28d7c88d467289e0587285d27adb172aecc5494a17df36",
        expand=False,
    )
    version(
        "4.7.2",
        sha256="6852386d7975eff29171dae002cc223251510d35f291ae277948f381a7b380b4",
        expand=False,
    )

    depends_on("java@8.0:", type="run", when="@4.10.0:")
    depends_on("java@7.0:", type="run", when="@:4.9.3")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        rename(glob.glob("antlr-*-complete.jar")[0], "antlr-complete.jar")
        install("antlr-complete.jar", prefix.bin)

    def setup_run_environment(self, env):
        env.set("ANTLR4_JAR_LOCATION", join_path(self.prefix.bin, "antlr-complete.jar"))
        env.set("ANTLR_JAR_LOCATION", join_path(self.prefix.bin, "antlr-complete.jar"))
        env.set("ANTLR_EXECUTABLE", join_path(self.prefix.bin, "antlr-complete.jar"))

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Canu(MakefilePackage):
    """A single molecule sequence assembler for genomes large and
    small."""

    homepage = "https://canu.readthedocs.io/"
    url = "https://github.com/marbl/canu/archive/v1.5.tar.gz"

    license("GPL-2.0-only")

    version(
        "2.2",
        sha256="e4d0c7b82149114f442ccd39e18f7fe2061c63b28d53700ad896e022b73b7404",
        url="https://github.com/marbl/canu/releases/download/v2.2/canu-2.2.tar.xz",
    )
    version("2.0", sha256="e2e6e8b5ec4dd4cfba5e372f4a64b2c01fbd544d4b5867746021f10771a6f4ef")
    version("1.8", sha256="30ecfe574166f54f79606038830f68927cf0efab33bdc3c6e43fd1448fa0b2e4")
    version("1.7.1", sha256="c314659c929ee05fd413274f391463a93f19b8337eabb7ee5de1ecfc061caafa")
    version("1.7", sha256="c5be54b0ad20729093413e7e722a19637d32e966dc8ecd2b579ba3e4958d378a")
    version("1.5", sha256="06e2c6d7b9f6d325b3b468e9c1a5de65e4689aed41154f2cee5ccd2cef0d5cf6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("git@2.12:", type="build", when="@2.2:")
    depends_on("gnuplot", type="run")
    depends_on("java", type="run")
    depends_on("perl", type="run")
    # version guessed from include date of vendored boost
    depends_on("boost@1.60.0:+graph")
    conflicts("^boost@1.70.1:", when="@:2.0")

    build_directory = "src"
    build_targets = ["clean"]

    def patch(self):
        # Use our perl, not whatever is in the environment
        filter_file(
            r"^#!/usr/bin/env perl",
            "#!{0}".format(self.spec["perl"].command.path),
            "src/pipelines/canu.pl",
        )

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("all", "TARGET_DIR={0}".format(prefix))

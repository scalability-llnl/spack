# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Primer3(MakefilePackage):
    """Primer3 is a widely used program for designing PCR primers
    (PCR = "Polymerase Chain Reaction"). PCR is an essential and
    ubiquitous tool in genetics and molecular biology. Primer3
    can also design hybridization probes and sequencing primers."""

    homepage = "https://primer3.org/"
    url = "https://github.com/primer3-org/primer3/archive/v2.3.7.tar.gz"

    license("GPL-2.0-only")

    version("2.6.1", sha256="805cef7ef39607cd40f0f5bb8b32e35e20007153a0a55131dd430ce644c8fb9e")
    version("2.5.0", sha256="7581e2fa3228ef0ee1ffa427b2aa0a18fc635d561208327471daf59d1b804da0")
    version("2.3.7", sha256="f7ac3e64dc89b7c80882bf0f52c2c0a58572f5fdafd178680d4a7ae91b6c465b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    build_directory = "src"

    # Prior to May 15, 2018, the code contained invalid pointer/int
    # comparisons, leading to compilers that default to strict mode
    # failing to compile thal.c.
    # This prevents building 2.3.7 w/ gcc@8.4.0.  Details here:
    # https://github.com/primer3-org/primer3/issues/2
    # https://github.com/primer3-org/primer3/issues/3
    def patch(self):
        if self.spec.version == Version("2.3.7"):
            filter_file(r"^(CC_OPTS.*)", r"\1 -fpermissive", join_path("src", "Makefile"))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            for binary in ("primer3_core", "ntdpal", "oligotm", "long_seq_tm_test"):
                install(binary, prefix.bin)

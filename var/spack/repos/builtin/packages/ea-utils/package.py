# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class EaUtils(MakefilePackage):
    """Command-line tools for processing biological sequencing data. Barcode
    demultiplexing, adapter trimming, etc. Primarily written to support an
    Illumina based pipeline - but should work with any FASTQs."""

    homepage = "https://expressionanalysis.github.io/ea-utils/"
    url = "https://github.com/ExpressionAnalysis/ea-utils/archive/1.04.807.tar.gz"
    git = "https://github.com/ExpressionAnalysis/ea-utils.git"
    maintainers("snehring")

    version("2021-10-20", commit="10c21926a4dce4289d5052acfd73b8e744d4fede")
    version(
        "1.04.807",
        sha256="aa09d25e6aa7ae71d2ce4198a98e58d563f151f8ff248e4602fa437f12b8d05f",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("sparsehash")
    depends_on("zlib-api")
    depends_on("gsl")
    depends_on("bamtools")
    depends_on("perl", type=["build", "run"])

    build_directory = "clipper"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file("/usr", prefix, "Makefile")
            # remove tests from all rule
            filter_file(r"^all:.*$", "all: $(BIN)", "Makefile")
            # remove the vendored sparsehash
            filter_file(" sparsehash", "", "Makefile")
            # replace system perl references
            for f in next(os.walk(os.getcwd()))[2]:
                filter_file("/usr/bin/perl", spec["perl"].prefix.bin.perl, f)
            # fix up test script require path
            tests = ["join.t", "mcf.t", "multx.t"]
            rep = 'require "{0}";'.format(os.path.join(os.getcwd(), "t", "test-prep.pl"))
            for f in tests:
                filter_file(r"^require.*$", rep, os.path.join(os.getcwd(), "t", f))

    def flag_handler(self, name, flags):
        if name.lower() == "cxxflags":
            flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)

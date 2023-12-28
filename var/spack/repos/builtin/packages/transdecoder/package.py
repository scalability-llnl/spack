# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Transdecoder(MakefilePackage):
    """TransDecoder identifies candidate coding regions within transcript
    sequences, such as those generated by de novo RNA-Seq transcript
    assembly using Trinity, or constructed based on RNA-Seq alignments to
    the genome using Tophat and Cufflinks."""

    homepage = "https://transdecoder.github.io/"
    url = "https://github.com/TransDecoder/TransDecoder/archive/TransDecoder-v5.5.0.tar.gz"

    license("BSD-3-Clause")

    version("5.7.1", sha256="41dd5e95f6ba946ff21340417d867e5e99f123b4035779b25d3cffd20b828a30")
    version("5.7.0", sha256="421b50dd08b12a88f2f09922e20c50903e335f26947843d9f925f5c0e9ddd79f")
    version("5.5.0", sha256="c800d9226350817471e9f51267c91f7cab99dbc9b26c980527fc1019e7d90a76")
    version(
        "3.0.1",
        sha256="753a5fac5bfd04466aeabff48053c92e876cece8906b96de3b72f23f86fafae7",
        url="https://github.com/TransDecoder/TransDecoder/archive/v3.0.1.tar.gz",
    )

    depends_on("perl", type=("build", "run"))
    depends_on("perl-uri", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.util)
        install("TransDecoder.LongOrfs", prefix)
        install("TransDecoder.Predict", prefix)
        install_tree("PerlLib", prefix.PerlLib)
        install_tree("util", prefix.util)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
        env.prepend_path("PATH", self.prefix.util)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class RnaSeqc(Package):
    """RNA-SeQC is a java program which computes a series of quality control
    metrics for RNA-seq data."""

    homepage = "http://archive.broadinstitute.org/cancer/cga/rna-seqc"
    url = "http://www.broadinstitute.org/cancer/cga/tools/rnaseqc/RNA-SeQC_v1.1.8.jar"

    version(
        "1.1.8",
        sha256="0a6a8cc885e77c7e7b75dafcfd2152e0d1031fa7aba2565250a46fbd98979793",
        expand=False,
    )
    version(
        "1.1.7",
        sha256="78e043a2973fed8d567e16bd1f68b1bd78dafe536a41cee07c32e3148e1f1ff3",
        expand=False,
    )
    version(
        "1.1.6",
        sha256="76f1497b275c801d18a1b403336569552853dd248d94aa625862ea08c6ba25f6",
        expand=False,
    )
    version(
        "1.1.5",
        sha256="1da100182037f46c61f93a063083e3be579da2678b0441fbc3fc8b58120e52c9",
        expand=False,
    )
    version(
        "1.1.4",
        sha256="eac437061157036dddf496be8e05fe62b011fb95d34e9079c93ee4001710f1c6",
        expand=False,
    )

    depends_on("java@8:", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = "RNA-SeQC_v{0}.jar".format(self.version.dotted)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "rna-seqc.sh")
        script = join_path(prefix.bin, "rna-seqc")
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)
        filter_file("RNA-SeQC_v{0}.jar", join_path(prefix.bin, jar_file), script, **kwargs)

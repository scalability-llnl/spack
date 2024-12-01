# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shortbred(Package):
    """ShortBRED is a system for profiling protein families of interest at
    very high specificity in shotgun meta'omic sequencing data."""

    homepage = "https://huttenhower.sph.harvard.edu/shortbred"
    url = "https://bitbucket.org/biobakery/shortbred/get/0.9.4.tar.gz"

    version(
        "0.9.4",
        sha256="a85e5609db79696d3f2d478408fc6abfeea7628de9f533c4e1e0ea3622b397ba",
        deprecated=True,
    )

    depends_on("blast-plus@2.2.28:")
    depends_on("cdhit@4.6:")
    depends_on("muscle@3.8.31:")
    depends_on("python@2.7.9:")
    depends_on("py-biopython")
    depends_on("usearch@6.0.307:")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("shortbred_identify.py", prefix.bin)
        install("shortbred_quantify.py", prefix.bin)
        install_tree("src", prefix.src)

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix)

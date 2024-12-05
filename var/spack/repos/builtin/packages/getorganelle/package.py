# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Getorganelle(PythonPackage):
    """Organelle Genome Assembly Toolkit (Chloroplast/Mitocondrial/ITS)"""

    homepage = "https://github.com/Kinggerm/GetOrganelle"
    url = "https://github.com/Kinggerm/GetOrganelle/archive/refs/tags/1.7.5.0.tar.gz"

    maintainers("snehring")

    license("GPL-3.0-only")

    version("1.7.7.0", sha256="dd351b5cd33688adfcd8bff9794ae0cc0ce01a572dac2bcf6c9d7db77b3e4883")
    version("1.7.5.0", sha256="c498196737726cb4c0158f23037bf301a069f5028ece729bb4d09c7d915df93d")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.16.4:", type=("build", "run"))
    depends_on("py-scipy@1.3.0:", type=("build", "run"))
    depends_on("py-sympy@1.4:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))

    depends_on("bowtie2", type="run")
    depends_on("spades", type="run")
    depends_on("blast-plus", type="run")

    # Allow access to relevant runtime scripts
    # I.e. get_organelle_config.py, get_organelle_from_reads.py, etc.
    def setup_run_environment(self, env):
        env.prepend_path("PATH", prefix)
        env.prepend_path("PATH", prefix.Utilities)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Busco(PythonPackage):
    """Assesses genome assembly and annotation completeness with Benchmarking
    Universal Single-Copy Orthologs"""

    homepage = "https://busco.ezlab.org/"
    url = "https://gitlab.com/api/v4/projects/ezlab%2Fbusco/repository/archive.tar.gz?sha=2.0.1"
    git = "https://gitlab.com/ezlab/busco.git"
    maintainers("snehring")

    license("MIT")

    version("5.4.3", sha256="8b92dcc32691f7c1629aaaa7bd54f96073273ba7de5a3a8586fe552c51a9d36a")
    version("4.1.3", sha256="08ded26aeb4f6aef791cd88524c3c00792a054c7672ea05219f468d495e7b072")

    # TODO: check the installation procedure for version 3.0.2
    # and uncomment the following line
    # version('3.0.2', sha256='dbea093315b766b0f7c4fe3cafbbdf51ade79ec84bde04f1f437b48333200f34')

    # There is no tag for version 3.0.1
    version("3.0.1", commit="078252e00399550d7b0e8941cd4d986c8e868a83")
    version("2.0.1", sha256="bd72a79b880370e9b61b8c722e171818c7c85d46cc1e2f80595df2738a7e220c")

    # https://busco.ezlab.org/busco_userguide.html#manual-installation
    depends_on("python@3.3:", when="@4:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", when="@3:", type="build")
    depends_on("blast-plus")
    depends_on("hmmer")
    depends_on("augustus")
    depends_on("py-biopython", when="@4.1.3:", type=("build", "run"))
    depends_on("py-pandas", when="@5:", type="run")
    depends_on("bbmap", when="@5:", type="run")
    depends_on("prodigal", when="@5:", type="run")
    depends_on("metaeuk", when="@5:", type="run")
    depends_on("sepp", when="@5:", type="run")

    def install(self, spec, prefix):
        if self.spec.satisfies("@4.1.3:"):
            install_tree("bin", prefix.bin)
            install_tree("config", prefix.config)
            super().install(spec, prefix)
        if self.spec.satisfies("@3.0.1"):
            with working_dir("scripts"):
                mkdirp(prefix.bin)
                install("generate_plot.py", prefix.bin)
                install("run_BUSCO.py", prefix.bin)
            install_tree("config", prefix.config)
            super().install(spec, prefix)
        if self.spec.satisfies("@2.0.1"):
            mkdirp(prefix.bin)
            install("BUSCO.py", prefix.bin)
            install("BUSCO_plot.py", prefix.bin)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPhydms(PythonPackage):
    """phydms enables phylogenetic analyses using deep mutational scanning data
    to inform the substitution models. It implements Experimentally informed
    codon models (ExpCM) for phylogenetic inference and the detection of
    biologically interesting selection."""

    homepage = "http://jbloomlab.github.io/phydms"
    pypi = "phydms/phydms-2.4.1.tar.gz"

    license("GPL-3.0-or-later")

    version("2.4.1", sha256="04eb50bdb07907214050d19214d9bc8cf2002e24ca30fbe6e0f23f013d584d5c")

    depends_on("c", type="build")  # generated

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-biopython@1.67:", type=("build", "run"))
    depends_on("py-cython@0.28:", type=("build", "run"))
    depends_on("py-numpy@1.16.5:", type=("build", "run"))
    depends_on("py-scipy@0.18:", type=("build", "run"))
    depends_on("py-matplotlib@2.0.2:", type=("build", "run"))
    depends_on("py-natsort@5.0.1:", type=("build", "run"))
    depends_on("py-sympy@1.0:", type=("build", "run"))
    depends_on("py-six@1.10:", type=("build", "run"))
    depends_on("py-pandas@0.20.2:", type=("build", "run"))
    depends_on("py-pyvolve@1.0.3:", type=("build", "run"))
    depends_on("py-statsmodels@0.8:", type=("build", "run"))
    depends_on("py-weblogo@3.4:3.5", type=("build", "run"))
    depends_on("py-pypdf2@1.26:", type=("build", "run"))

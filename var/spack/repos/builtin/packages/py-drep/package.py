# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDrep(PythonPackage):
    """dRep is a python program for rapidly comparing large numbers of genomes.
    dRep can also "de-replicate" a genome set by identifying groups of highly
    similar genomes and choosing the best representative genome for each
    genome set."""

    homepage = "https://github.com/MrOlm/drep"
    pypi = "drep/drep-3.4.0.tar.gz"

    maintainers("MrOlm")

    license("MIT")

    version("3.4.2", sha256="90d61e40b987cef85b52209720afe15c090d6af8095f5ac8d14354b374007fa7")
    version("3.4.0", sha256="a6533eb585122c1ee66ae622b1b97450a3e1e493a3c3c1d55e79a580d5c46d40")

    variant("fastani", default=True, description="Enable fastANI support")
    variant("py-checkm-genome", default=True, description="Enable CheckM support")
    variant("anicalculator", default=True, description="Enable gDNA support")
    variant("prodigal", default=True, description="Used with both checkM and gANI")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pytest", type=("build", "run"))
    # Non-python dependencies
    # https://drep.readthedocs.io/en/latest/installation.html#dependencies
    # essential dependencies
    depends_on("mash@1.1.1:", type="run")
    depends_on("mummer@3.23:", type="run")
    # recommended dependencies
    depends_on("fastani", type="run", when="+fastani")
    depends_on("py-checkm-genome@1.0.7:", type="run", when="+py-checkm-genome")
    depends_on("anicalculator@1:", type="run", when="+anicalculator")
    depends_on("prodigal@2.6.3:", type="run", when="+prodigal")

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAnvio(PythonPackage):
    """"Anvi’o is a comprehensive platform that brings together many aspects of
    today’s cutting-edge computational strategies of data-enabled microbiology,
    including genomics, metagenomics, metatranscriptomics, pangenomics,
    metapangenomics, phylogenomics, and microbial population genetics in an
    integrated and easy-to-use fashion through extensive interactive
    visualization capabilities."""

    homepage = "https://anvio.org/"

    # Not available on pypi
    url = "https://github.com/merenlab/anvio/releases/download/v8/anvio-8.tar.gz"

    version("8", sha256="13da84d48d7266a8986815efb024772fa26ad1c8a951d42897c3a51e3d924feb")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@:1.24", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-bottle", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-ete3", type=("build", "run"))
    depends_on("py-scikit-learn@1.2.2", type=("build", "run"))
    depends_on("py-django", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-mistune", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-statsmodels", type=("build", "run"))
    depends_on("py-colored", type=("build", "run"))
    depends_on("py-illumina-utils", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-rich-argparse", type=("build", "run"))
    depends_on("py-numba", type=("build", "run"))
    depends_on("py-paste", type=("build", "run"))
    depends_on("py-pyani", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pandas@1.4.4", type=("build", "run"))
    depends_on("snakemake", type=("build", "run"))
    depends_on("py-multiprocess", type=("build", "run"))
    depends_on("py-plotext", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))

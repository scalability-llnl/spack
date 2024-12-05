# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonLouvain(PythonPackage):
    """This module implements community detection.
    It uses the louvain method described in Fast unfolding of communities
    in large networks, Vincent D Blondel, Jean-Loup Guillaume, Renaud
    Lambiotte, Renaud Lefebvre, Journal of Statistical Mechanics: Theory
    and Experiment 2008(10), P10008 (12pp)"""

    homepage = "https://github.com/taynaud/python-louvain"
    pypi = "python-louvain/python-louvain-0.14.tar.gz"

    license("BSD-3-Clause")

    version("0.15", sha256="2a856edfbe29952a60a5538a84bb78cca18f6884a88b9325e85a11c8dd4917eb")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))

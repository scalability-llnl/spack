# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMarkovClustering(PythonPackage):
    """Implementation of the Markov clustering (MCL) algorithm in python"""

    homepage = "https://github.com/GuyAllard/markov_clustering"
    pypi = "markov_clustering/markov_clustering-0.0.6.dev0.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version(
        "0.0.6.dev0", sha256="8f72eee0ee5d9bfbab1b28bbfa95eaa020b2bba64b528ce45030b8b4300ecf33"
    )

    variant("drawing", default=False, description="Include graphing capabilities")

    depends_on("python@3", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy@0.19.0:", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))

    depends_on("py-networkx", type=("build", "run"), when="+drawing")
    depends_on("py-matplotlib", type=("build", "run"), when="+drawing")

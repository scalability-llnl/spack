# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonIgraph(PythonPackage):
    """igraph is a collection of network analysis tools with the emphasis on
    efficiency, portability and ease of use."""

    homepage = "https://igraph.org/"
    url = "https://igraph.org/nightly/get/python/python-igraph-0.7.0.tar.gz"

    license("GPL-2.0-or-later")

    version("0.7.0", sha256="64ac270e80a92066d489407be1900a329df8e26844430f941ecc88771188c471")

    depends_on("py-setuptools", type="build")
    depends_on("igraph")

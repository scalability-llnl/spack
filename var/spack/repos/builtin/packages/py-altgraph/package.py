# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAltgraph(PythonPackage):
    """
    altgraph is a fork of graphlib: a graph (network)
    package for constructing graphs, BFS and DFS traversals,
    topological sort, shortest paths, etc. with graphviz output.
    """

    pypi = "altgraph/altgraph-0.16.1.tar.gz"

    license("MIT")

    version("0.16.1", sha256="ddf5320017147ba7b810198e0b6619bd7b5563aa034da388cea8546b877f9b0c")

    depends_on("py-setuptools", type="build")

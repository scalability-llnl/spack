# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastpath(PythonPackage):
    """Fastpath is a fast and lightweight tool for finding the shortest path in
    a weighted graph. As input it only needs the starting node, the ending node,
    and the weights of each node to node edge."""

    homepage = "https://github.com/deprekate/fastpath"
    pypi = "fastpath/fastpath-1.9.tar.gz"

    license("GPL-3.0-only")

    version("1.9", sha256="3372d306a3c4e4e764b3995946132333726a229e9002879b9112779dd442b31a")

    depends_on("c", type="build")  # generated

    depends_on("python@3.5.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

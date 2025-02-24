# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrodigal(PythonPackage):
    """Cython bindings and Python interface to Prodigal, an ORF finder for
    genomes and metagenomes"""

    homepage = "https://github.com/althonos/pyrodigal"
    pypi = "pyrodigal/pyrodigal-3.5.2.tar.gz"

    license("GPL-3.0", checked_by="luke-dt")

    version("3.5.2", sha256="2a40eb6113e720ada51c326958b295944cdc33ecee9f25d5bad4e9a8e6e6f7f5")

    depends_on("c", type="build")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@46.4:", type="build")
    depends_on("py-archspec@0.2.0:", type="build")
    depends_on("py-cython@3.0:", type=("build", "run"))

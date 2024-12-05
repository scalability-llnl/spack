# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBasisSetExchange(PythonPackage):
    """Command-line interface for the Basis Set Exchange Website"""

    homepage = "https://www.basissetexchange.org"
    url = "https://github.com/MolSSI-BSE/basis_set_exchange/archive/v0.8.12.tar.gz"

    maintainers("bennybp", "scemama")

    license("BSD-3-Clause")

    version("0.8.12", sha256="41f0242e2c11392c511d3308c0345e14b0eb3344686d865bdfcb48257910fc0d")
    version("0.8.11", sha256="dbd4cf9382d97b79a3143c6b2086d1d24562bd13e0ab0d18fc0423b9ee877b9b")
    version("0.8.10", sha256="7f974faf513791d59ef47dd4eba9d8386f75bbd85f253ca5c08732ff56004a57")
    version("0.8.9", sha256="faf01a00c8ef7cf7331562052fbf1ff861e901545a927310ab09ac03604b400b")
    version("0.8.8", sha256="4770bc901b93bfbf1aa5e1c4b486804753b3ff19c41794d3200ffe990b12dfa1")
    version("0.8.7", sha256="5e9e18ca84bd378d1e02b6543cee122d8cc4efeaf05b1801061b500dda4cb2fc")
    version("0.8.6", sha256="96da4ab45adaab11825917dc4cf0e236f5d2f0af0f2e026578262ce389784912")
    version("0.8.5", sha256="ff8e6e03474319245e641c9da05715a6ea90dccab0e60ad2b0bc8556f85a9bca")
    version("0.8.4", sha256="005f95794ce55f1b1e8faa0b6910b814819dd4ee9dba367a3ec29dfe53816684")
    version("0.8.3", sha256="0721f3cf55f588f62d74a408bccdd44046ebeaab8ec802c02fae7983d8f0359f")

    depends_on("py-argcomplete", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("python@3:", type=("build", "run"))

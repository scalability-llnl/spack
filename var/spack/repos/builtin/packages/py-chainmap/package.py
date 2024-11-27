# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChainmap(PythonPackage):
    """Clone/backport of ChainMap for Python 2.6, Python 3.2, and PyPy3
    based on Python 3.2--versions that currently lack their own
    ChainMap implementations."""

    homepage = "https://bitbucket.org/jeunice/chainmap/src/default/"
    pypi = "chainmap/chainmap-1.0.3.tar.gz"

    version("1.0.3", sha256="e42aaa4b3e2f66102a11bfd563069704bfbfd84fdcb517b564effd736bf53cd9")
    version("1.0.2", sha256="405da3bce9913bfb33e6e497803b447b60d12ab44031ca357626143e087e0526")
    version("1.0.1", sha256="c1cd76c679dd7af982ec5a45788ef4a0dfc20e77f27ccdeca289a5141862ff64")
    version("1.0.0", sha256="2e24b2efa3494b16772282812efcd712b1d6b80e1b761a56b1b7cbc8fe0313c4")

    depends_on("py-setuptools", type="build")

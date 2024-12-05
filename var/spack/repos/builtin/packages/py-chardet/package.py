# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChardet(PythonPackage):
    """Universal encoding detector for Python 3"""

    homepage = "https://github.com/chardet/chardet"
    pypi = "chardet/chardet-3.0.4.tar.gz"

    license("LGPL-2.1-or-later")

    version("5.2.0", sha256="1b3b6ff479a8c414bc3fa2c0852995695c4a026dcd6d0633b2dd092ca39c1cf7")
    version("5.1.0", sha256="0d62712b956bc154f85fb0a266e2a3c5913c2967e00348701b32411d6def31e5")
    version("5.0.0", sha256="0368df2bfd78b5fc20572bb4e9bb7fb53e2c094f60ae9993339e8671d0afb8aa")
    version("4.0.0", sha256="0d6f53a15db4120f2b08c94f11e7d93d2c911ee118b6b30a04ec3ee8310179fa")
    version("3.0.4", sha256="84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae")
    version("3.0.2", sha256="4f7832e7c583348a9eddd927ee8514b3bf717c061f57b21dbe7697211454d9bb")
    version("2.3.0", sha256="e53e38b3a4afe6d1132de62b7400a4ac363452dc5dfcf8d88e8e0cce663c68aa")

    depends_on("py-setuptools", type="build")

    # Historical dependencies
    depends_on("py-pytest-runner", when="@3", type="build")

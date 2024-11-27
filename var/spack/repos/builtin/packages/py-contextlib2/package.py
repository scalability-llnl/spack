# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyContextlib2(PythonPackage):
    """contextlib2 is a backport of the standard library's contextlib module to
    earlier Python versions."""

    homepage = "https://contextlib2.readthedocs.io/en/stable/"
    pypi = "contextlib2/contextlib2-21.6.0.tar.gz"

    license("PSF-2.0")

    version("21.6.0", sha256="ab1e2bfe1d01d968e1b7e8d9023bc51ef3509bba217bb730cee3827e1ee82869")
    version("0.6.0", sha256="7197aa736777caac513dbd800944c209a49765bf1979b12b037dce0277077ed3")
    version("0.5.5", sha256="509f9419ee91cdd00ba34443217d5ca51f5a364a404e1dce9e8979cea969ca48")

    depends_on("py-setuptools", type="build")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@21.6.0:")

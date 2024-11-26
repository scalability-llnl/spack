# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLazyObjectProxy(PythonPackage):
    """A fast and thorough lazy object proxy."""

    homepage = "https://github.com/ionelmc/python-lazy-object-proxy"
    pypi = "lazy-object-proxy/lazy-object-proxy-1.3.1.tar.gz"

    license("BSD-2-Clause")

    version("1.7.1", sha256="d609c75b986def706743cdebe5e47553f4a5a1da9c5ff66d76013ef396b5a8a4")
    version("1.7.0", sha256="2185392631e9d1733749d06ee5210438908d46cc04666a0eba5679d885754894")
    version("1.6.0", sha256="489000d368377571c6f982fba6497f2aa13c6d1facc40660963da62f5c379726")
    version("1.4.3", sha256="f3900e8a5de27447acbf900b4750b0ddfd7ec1ea7fbaf11dfa911141bc522af0")
    version("1.3.1", sha256="eb91be369f945f10d3a49f5f9be8b3d0b93a4c2be8f8a5b83b0571b8123e0a7a")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.6:", type=("build", "run"), when="@1.6.0:")
    depends_on("python@3.6:", type=("build", "run"), when="@1.7.0:")

    depends_on("py-setuptools-scm@3.3.1:", type="build", when="@1.4.0:")
    depends_on("py-setuptools-scm@3.3.1:5", type="build", when="@1.6.0:1.6")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@30.3.0:", type="build", when="@1.6.0:")

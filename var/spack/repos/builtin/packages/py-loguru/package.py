# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLoguru(PythonPackage):
    """Loguru is a library which aims to bring enjoyable logging in Python."""

    homepage = "https://github.com/Delgan/loguru"
    pypi = "loguru/loguru-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="066bd06758d0a513e9836fd9c6b5a75bfb3fd36841f4b996bc60b547a309d41c")
    version("0.3.0", sha256="f2a0fa92f334d37a13351aa36ab18e8039649a3741836b4b6d8b8bce7e8457ac")
    version("0.2.5", sha256="68297d9f23064c2f4764bb5d0c5c767f3ed7f9fc1218244841878f5fc7c94add")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-aiocontextvars@0.2.0:", when="^python@3.6:", type=("build", "run"))
    depends_on("py-colorama@0.3.4:", when="platform=windows", type=("build", "run"))
    # Missing dependency required for windows
    # depends_on('py-win32-setctime@1.0.0:',
    #            when='platform=windows',
    #            type=('build', 'run'))
    conflicts("platform=windows")

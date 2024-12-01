# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQtawesome(PythonPackage):
    """FontAwesome icons in PyQt and PySide applications"""

    homepage = "https://github.com/spyder-ide/qtawesome"
    pypi = "QtAwesome/QtAwesome-0.4.1.tar.gz"

    license("MIT")

    version("0.4.1", sha256="9ea91efeb83e8b73f814aeca898c29cade0c087acec58e91b4f384595aeb4cfd")
    version("0.3.3", sha256="c3c98ee4df0133ae42d202fea20253f8746266b4541c5df4269ca4131792ce0f")

    depends_on("py-setuptools", type="build")
    depends_on("py-qtpy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))

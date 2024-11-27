# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyvue(PythonPackage):
    """
    Jupyter widgets base for Vue libraries.
    """

    homepage = "https://github.com/widgetti/ipyvue"
    pypi = "ipyvue/ipyvue-1.10.1.tar.gz"

    license("MIT")

    maintainers("jeremyfix")

    version("1.10.1", sha256="20615ce86ba516cf0b7aad84cc607e4e2c9104232e954cd0eccbf33530a5e1d4")

    depends_on("py-setuptools", type="build")

    depends_on("py-ipywidgets@7:", type=("build", "run"))

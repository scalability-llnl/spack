# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonDocsTheme(PythonPackage):
    """This is the theme for the Python documentation."""

    homepage = "https://docs.python.org/3/"
    pypi = "python-docs-theme/python-docs-theme-2018.7.tar.gz"

    license("PSF-2.0")

    version("2020.1", sha256="29c33ba393bdb9377910116a0c1cc329573a4e040227c58a3293d27928d8262a")
    version("2018.7", sha256="018a5bf2a7318c9c9a8346303dac8afc6bc212d92e86561c9b95a3372714155a")

    depends_on("py-setuptools")

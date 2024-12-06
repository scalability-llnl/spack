# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbval(PythonPackage):
    """Py.test plugin for validating Jupyter notebooks.

    The plugin adds functionality to py.test to recognise and collect Jupyter notebooks.
    The intended purpose of the tests is to determine whether execution of the stored
    inputs match the stored outputs of the .ipynb file. Whilst also ensuring that the
    notebooks are running without errors.
    """

    homepage = "https://github.com/computationalmodelling/nbval"
    pypi = "nbval/nbval-0.9.6.tar.gz"

    license("BSD-3-Clause")

    version("0.9.6", sha256="cfefcd2ef66ee2d337d0b252c6bcec4023384eb32e8b9e5fcc3ac80ab8cd7d40")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@2.8:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-jupyter-client", type=("build", "run"))
    depends_on("py-nbformat", type=("build", "run"))
    depends_on("py-ipykernel", type=("build", "run"))
    depends_on("py-coverage", type=("build", "run"))

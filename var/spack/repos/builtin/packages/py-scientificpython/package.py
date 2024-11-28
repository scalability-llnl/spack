# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScientificpython(PythonPackage):
    """ScientificPython is a collection of Python modules for
    scientific computing. It contains support for geometry,
    mathematical functions, statistics, physical units, IO,
    visualization, and parallelization."""

    homepage = "https://sourcesup.renater.fr/projects/scientific-py/"
    url = "https://sourcesup.renater.fr/frs/download.php/file/4411/ScientificPython-2.8.1.tar.gz"

    license("CECILL-C")

    version("2.8.1", sha256="d9ef354736410bbb2e8be33cb7433cf62114307a44e3a96baaa793b58b4b518b")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))

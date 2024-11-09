# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyke(PythonPackage):
    """Pyke introduces a form of Logic Programming (inspired by Prolog)
    to the Python community by providing a knowledge-based inference
    engine (expert system) written in 100% Python.
    """

    homepage = "https://sourceforge.net/projects/pyke/"
    url = "https://sourceforge.net/projects/pyke/files/pyke/1.1.1/pyke-1.1.1.zip"

    license("MIT")

    version("1.1.1", sha256="b0b294f435c6e6d2d4a80badf57d92cb66814dfe21e644a521901209e6a3f8ae")

    depends_on("python@3:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")

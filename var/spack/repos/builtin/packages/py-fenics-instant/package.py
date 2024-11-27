# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsInstant(PythonPackage):
    """Instant is a Python module that allows for instant inlining of C and C++
    code in Python. It is a small Python module built on top of SWIG and
    Distutils. Instant has been retired after 2017.2.0 release. It is no longer
    needed in FEniCS and hence no longer maintained and tested."""

    homepage = "https://fenicsproject.org"
    url = "https://bitbucket.org/fenics-project/instant/downloads/instant-2017.2.0.tar.gz"
    maintainers("emai-imcs")

    license("LGPL-3.0-or-later")

    version("2017.2.0", sha256="be24f162fd1a89b82fae002db8df0b4f111fd50db83d78c0c121015c02e45b7b")
    version("2016.2.0", sha256="df5e8ca306546fd1ee1a28e36b61c5d46456dc8b07e3293d674ddff62cf8d953")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("cmake", type="run")
    depends_on("swig", type=("build", "run"))

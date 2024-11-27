# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyF90wrap(PythonPackage):
    """f90wrap is a tool to automatically generate Python extension
    modules which interface to Fortran code that makes use of derived types."""

    homepage = "https://github.com/jameskermode/f90wrap"
    pypi = "f90wrap/f90wrap-0.2.3.tar.gz"

    license("LGPL-3.0-only")

    version("0.2.6", sha256="e0748eb5e288be7f47829a272fc230373469fb40afccddf91e9973c56da43dd4")
    version("0.2.3", sha256="5577ea92934c5aad378df21fb0805b5fb433d6f2b8b9c1bf1a9ec1e3bf842cff")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # TODO errors with python 3.6 due to UnicodeDecodeError
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.3.0:", type=("build", "run"))

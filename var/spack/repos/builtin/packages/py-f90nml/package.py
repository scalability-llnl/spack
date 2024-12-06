# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyF90nml(PythonPackage):
    """Fortran 90 namelist parser."""

    homepage = "https://github.com/marshallward/f90nml"
    pypi = "f90nml/f90nml-1.4.3.tar.gz"

    version("1.4.3", sha256="e2f3cd23d821ebcaef66ce406485b35aa08aae0df92c4bece76e227e5bd146e1")
    version("1.4.1", sha256="9df312aa13b9c21936f059cab9ab40afebc280f1ab54e6854c3873d0b7b7865c")
    version("1.3.1", sha256="145c1f2c55bad628d225af22fc9bf06347eb0d33e7bae8a05869a68274b8fb2d")

    depends_on("py-setuptools", type="build")

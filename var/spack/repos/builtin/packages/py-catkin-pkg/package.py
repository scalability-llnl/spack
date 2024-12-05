# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCatkinPkg(PythonPackage):
    """Library for retrieving information about catkin packages."""

    homepage = "https://wiki.ros.org/catkin_pkg"
    pypi = "catkin-pkg/catkin_pkg-0.4.23.tar.gz"

    version("0.4.23", sha256="28ee181cca827c0aabf9397351f58a97e1475ca5ac7c106a5916e3ee191cd3d0")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))

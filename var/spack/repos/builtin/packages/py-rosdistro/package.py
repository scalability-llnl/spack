# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRosdistro(PythonPackage):
    """A tool to work with rosdistro files."""

    homepage = "https://wiki.ros.org/rosdistro"
    pypi = "rosdistro/rosdistro-0.8.3.tar.gz"

    version("0.8.3", sha256="e14893e0408a2e1fb3ecaef0a9fc978a3675519b828c1fff29ba6a78299b37bd")

    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-catkin-pkg", type=("build", "run"))
    depends_on("py-rospkg", type=("build", "run"))

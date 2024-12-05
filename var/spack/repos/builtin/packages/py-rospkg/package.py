# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRospkg(PythonPackage):
    """Library for retrieving information about ROS packages and stacks."""

    homepage = "https://wiki.ros.org/rospkg"
    pypi = "rospkg/rospkg-1.2.9.tar.gz"

    version("1.2.9", sha256="d57aea0e7fdbf42e8189ef5e21b9fb4f8a70ecb6cd1a56a278eab301f6a2b074")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-catkin-pkg", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-distro", type=("build", "run"))

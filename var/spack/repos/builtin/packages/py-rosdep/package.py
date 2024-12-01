# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRosdep(PythonPackage):
    """rosdep package manager abstraction tool for ROS."""

    homepage = "https://wiki.ros.org/rosdep"
    pypi = "rosdep/rosdep-0.20.0.tar.gz"

    version("0.20.0", sha256="1de76e41ef17c7289a11d9de594f6c08e8422f26ad09bc855b4f1f4da5e9bfe7")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-catkin-pkg@0.4.0:", type=("build", "run"))
    depends_on("py-rospkg@1.2.7:", type=("build", "run"))
    depends_on("py-rosdistro@0.7.5:", type=("build", "run"))
    depends_on("py-pyyaml@3.1:", type=("build", "run"))

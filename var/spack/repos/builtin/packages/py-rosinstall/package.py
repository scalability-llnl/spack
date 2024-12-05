# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRosinstall(PythonPackage):
    """The installer for ROS."""

    homepage = "https://wiki.ros.org/rosinstall"
    pypi = "rosinstall/rosinstall-0.7.8.tar.gz"

    version("0.7.8", sha256="2ba808bf8bac2cc3f13af9745184b9714c1426e11d09eb96468611b2ad47ed40")

    depends_on("py-setuptools", type="build")
    depends_on("py-vcstools@0.1.38:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-rosdistro@0.3.0:", type=("build", "run"))
    depends_on("py-catkin-pkg", type=("build", "run"))
    depends_on("py-wstool@0.1.12:", type=("build", "run"))

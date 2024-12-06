# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRosinstallGenerator(PythonPackage):
    """A tool for generating rosinstall files."""

    homepage = "https://wiki.ros.org/rosinstall_generator"
    pypi = "rosinstall-generator/rosinstall_generator-0.1.22.tar.gz"

    version("0.1.22", sha256="22d22599cd3f08a1f77fb2b1d9464cc8062ede50752a75564d459fcf5447b8c5")

    depends_on("py-catkin-pkg@0.1.28:", type=("build", "run"))
    depends_on("py-rosdistro@0.7.3:", type=("build", "run"))
    depends_on("py-rospkg", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

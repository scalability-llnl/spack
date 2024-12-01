# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVirtualenvClone(PythonPackage):
    """A script for cloning a non-relocatable virtualenv."""

    homepage = "https://github.com/edwardgeorge/virtualenv-clone"
    pypi = "virtualenv-clone/virtualenv-clone-0.2.6.tar.gz"

    license("MIT")

    version("0.5.7", sha256="418ee935c36152f8f153c79824bb93eaf6f0f7984bae31d3f48f350b9183501a")
    version("0.2.6", sha256="6b3be5cab59e455f08c9eda573d23006b7d6fb41fae974ddaa2b275c93cc4405")

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("python@2.7:2,3.4:", type=("build", "run"), when="@0.5.7:")
    # not just build-time, requires pkg_resources
    depends_on("py-setuptools", type=("build", "run"))

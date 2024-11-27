# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygdal(PythonPackage):
    """
    Virtualenv and setuptools friendly version of standard GDAL python
    bindings.

    This package is for you if you had problems installing GDAL in your
    virtualenv. You can install GDAL into your virtualenv using this package
    but you still need to install GDAL library and its header files on your
    system.
    """

    homepage = "https://github.com/nextgis/pygdal"
    pypi = "pygdal/pygdal-3.0.1.5.tar.gz"

    license("MIT")

    version("3.3.2.10", sha256="7fb9eec8aeb36b94389ff9f2b40cdceffefc8c290d813f4908b4acd208ca3a84")
    version("3.3.0.10", sha256="ea0c20bee67fac94fe0b1cb604a4fd0dc600aa8aa15cf9a7b6dc76adeb48670e")
    version("3.0.4.6", sha256="8e39b58cd9465bb5f41786a7cf6a62df93334c104db05a5bfb8181a0be276b86")
    version("3.0.1.5", sha256="1222f69fe5e6b632d0d2a42d3acb8fac80fb4577c05e01969d8cd5548192ccaa")
    version("2.4.2.5", sha256="73386683c0b10ab43b6d64257fca2ba812f53ec61b268de8811565fd9ae9bacd")
    version("2.4.1.6", sha256="5d1af98ad09f59e34e3b332cf20630b532b33c7120295aaaabbccebf58a11aa4")
    version("2.4.0.6", sha256="728d11f3ecae0cd3493cd27dab599a0b6184f5504cc172d49400d88ea2b24a9c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:", when="@3.3:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.0.0:", type=("build", "run"))
    # pygdal's build only works with the specified gdal version
    depends_on("gdal@3.3.2", type=("build", "link", "run"), when="@3.3.2.10")
    depends_on("gdal@3.3.0", type=("build", "link", "run"), when="@3.3.0.10")
    depends_on("gdal@3.0.4", type=("build", "link", "run"), when="@3.0.4.6")
    depends_on("gdal@3.0.1", type=("build", "link", "run"), when="@3.0.1.5")
    depends_on("gdal@2.4.2", type=("build", "link", "run"), when="@2.4.2.5")
    depends_on("gdal@2.4.1", type=("build", "link", "run"), when="@2.4.1.6")
    depends_on("gdal@2.4.0", type=("build", "link", "run"), when="@2.4.0.6")

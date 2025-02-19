# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRegions(PythonPackage):
    """An Astropy coordinated package for region handling"""

    homepage = "https://github.com/astropy/regions"
    pypi = "regions/regions-0.10.tar.gz"

    license("BSD-3-Clause", checked_by="lgarrison")

    version("0.10", sha256="961c518ea044268de0003a17953de3d4984623e9d47ad5424c100f6967e69a81")

    variant("all", default=False, description="Install all optional dependencies")

    depends_on("c", type="build")

    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-setuptools@61.2:", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build")
    depends_on("py-cython@3.0.0:3.0", type="build")
    depends_on("py-numpy@2.0.0rc1:", type="build")
    depends_on("py-extension-helpers@1", type="build")

    depends_on("py-numpy@1.23:", type=("build", "run"))
    depends_on("py-astropy@5.1:", type=("build", "run"))

    depends_on("py-matplotlib@3.5:", type=("build", "run"), when="+all")
    depends_on("py-shapely", type=("build", "run"), when="+all")

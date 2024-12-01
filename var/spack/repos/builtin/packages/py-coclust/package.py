# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCoclust(PythonPackage):
    """Coclust provides both a Python package which implements several diagonal and
    non-diagonal co-clustering algorithms, and a ready to use script to perform co-
    clustering"""

    homepage = "https://github.com/franrole/cclust_package"
    pypi = "coclust/coclust-0.2.1.tar.gz"

    maintainers("meyersbs")

    version("0.2.1", sha256="47800cc71b91fcf5551252dca865ac2d917891afc458972c3a0bca0de4643cfb")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))

    variant("alldeps", default=False, description="matplotlib support")
    depends_on("py-matplotlib@1.5:", when="+alldeps", type=("build", "run"))

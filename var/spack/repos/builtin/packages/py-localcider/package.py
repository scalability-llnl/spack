# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLocalcider(PythonPackage):
    """Tools for calculating sequence properties of disordered proteins"""

    homepage = "https://pappulab.github.io/localCIDER"
    pypi = "localcider/localcider-0.1.14.tar.gz"

    license("GPL-2.0-or-later")

    version("0.1.14", sha256="54ff29e8a011947cca5df79e96f3c69a76c49c4db41dcf1608663992be3e3f5f")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

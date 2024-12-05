# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGravity(PythonPackage):
    """Command-line utilities to assist in managing Galaxy servers"""

    homepage = "https://github.com/galaxyproject/gravity"
    pypi = "gravity/gravity-0.13.6.tar.gz"

    license("MIT")

    version("0.13.6", sha256="6fc2377e7c61b7db9406fb5b5c70bf72c571fb777f1313fc98787ef4cd007394")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-click", type=("build", "run"))
    depends_on("py-supervisor", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-ruamel-yaml", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-jsonref", type=("build", "run"))

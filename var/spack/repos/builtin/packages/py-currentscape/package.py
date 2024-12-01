# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCurrentscape(PythonPackage):
    """Module to easily plot the currents in electrical neuron models."""

    homepage = "https://github.com/BlueBrain/Currentscape"
    git = "https://github.com/BlueBrain/Currentscape.git"
    pypi = "currentscape/currentscape-1.0.12.tar.gz"

    license("Apache-2.0")

    version("1.0.12", sha256="d83c5a58074e4d612553472a487e5d1d2854dc4d5c161817c6bafdf4a5988011")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type=("build",))
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-palettable", type=("build", "run"))

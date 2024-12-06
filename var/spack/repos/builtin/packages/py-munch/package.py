# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMunch(PythonPackage):
    """A Munch is a Python dictionary that provides attribute-style
    access (a la JavaScript objects)."""

    homepage = "https://github.com/Infinidat/munch"
    pypi = "munch/munch-2.5.0.tar.gz"

    license("MIT")

    version("2.5.0", sha256="2d735f6f24d4dba3417fa448cae40c6e896ec1fdab6cdb5e6510999758a4dbd2")
    version("2.2.0", sha256="62fb4fb318e965a464b088e6af52a63e0905a50500b770596a939d3855e7aa15")

    depends_on("py-pbr@3:", when="@2.5:", type="build")
    depends_on("py-setuptools@17.1:", when="@2.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))

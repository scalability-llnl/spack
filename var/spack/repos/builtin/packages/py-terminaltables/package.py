# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTerminaltables(PythonPackage):
    """Generate simple tables in terminals from a nested list of strings."""

    homepage = "https://github.com/Robpol86/terminaltables"
    pypi = "terminaltables/terminaltables-3.1.0.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("3.1.0", sha256="f3eb0eb92e3833972ac36796293ca0906e998dc3be91fbe1f8615b331b853b81")

    depends_on("py-setuptools", type="build")
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-termcolor", type=("build", "run"))
    depends_on("py-colorclass", type=("build", "run"))

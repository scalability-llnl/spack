# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTzlocal(PythonPackage):
    """tzinfo object for the local timezone."""

    homepage = "https://github.com/regebro/tzlocal"
    pypi = "tzlocal/tzlocal-1.3.tar.gz"

    license("MIT")

    version("2.1", sha256="643c97c5294aedc737780a49d9df30889321cbe1204eac2c2ec6134035a92e44")
    version("2.0.0", sha256="949b9dd5ba4be17190a80c0268167d7e6c92c62b30026cf9764caf3e308e5590")
    version("1.3", sha256="d160c2ce4f8b1831dabfe766bd844cf9012f766539cf84139c2faac5201882ce")

    depends_on("py-setuptools", type="build")

    depends_on("py-pytz", type=("build", "run"))

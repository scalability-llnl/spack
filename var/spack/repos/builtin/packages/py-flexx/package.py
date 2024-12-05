# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlexx(PythonPackage):
    """Write desktop and web apps in pure Python."""

    homepage = "https://flexx.readthedocs.io"
    pypi = "flexx/flexx-0.4.1.zip"

    version("0.4.1", sha256="54be868f01d943018d0907821f2562f6eb31c568b3932abfd8518f75c29b8be1")

    depends_on("py-setuptools", type="build")
    depends_on("py-tornado", type=("build", "run"))

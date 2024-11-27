# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySingledispatchmethod(PythonPackage):
    """Backport of functools.singledispatchmethod to Python 2.7-3.7."""

    homepage = "https://github.com/ikalnytskyi/singledispatchmethod"
    pypi = "singledispatchmethod/singledispatchmethod-1.0.tar.gz"

    license("MIT")

    version("1.0", sha256="183a7fbeab53b9c9d182f8b8f9c2d7e109a7d40afaa30261d81dd8de68cd73bf")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

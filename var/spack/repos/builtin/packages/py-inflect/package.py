# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInflect(PythonPackage):
    """inflect.py - Correctly generate plurals, singular nouns, ordinals,
    indefinite articles; convert numbers to words."""

    homepage = "https://github.com/jaraco/inflect"
    pypi = "inflect/inflect-5.0.2.tar.gz"

    license("MIT")

    version("6.0.2", sha256="f1a6bcb0105046f89619fde1a7d044c612c614c2d85ef182582d9dc9b86d309a")
    version("5.0.2", sha256="d284c905414fe37c050734c8600fe170adfb98ba40f72fc66fed393f5b8d5ea0")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"), when="@6.0.2:")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools@56:", type="build", when="@6.0.2:")
    depends_on("py-setuptools-scm+toml@3.4.1:", type="build")
    depends_on("py-pydantic@1.9.1:", type=("build", "run"), when="@6.0.2:")

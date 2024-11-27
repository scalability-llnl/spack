# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsCachedProperty(PythonPackage):
    """cached_property() - computed once per instance, cached as attribute"""

    homepage = "https://github.com/penguinolog/backports.cached_property"
    pypi = "backports.cached-property/backports.cached-property-1.0.2.tar.gz"

    license("MIT")

    version("1.0.2", sha256="9306f9eed6ec55fd156ace6bc1094e2c86fae5fb2bf07b6a9c00745c656e75dd")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPystache(PythonPackage):
    """Pystache is a Python implementation of Mustache. Mustache is a
    framework-agnostic, logic-free templating system inspired by ctemplate and
    et."""

    homepage = "https://github.com/sarnold/pystache"
    git = "https://github.com/sarnold/pystache"
    pypi = "pystache/pystache-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="93bf92b2149a4c4b58d12142e2c4c6dd5c08d89e4c95afccd4b6efe2ee1d470d")

    depends_on("py-setuptools@40.8:", type="build")

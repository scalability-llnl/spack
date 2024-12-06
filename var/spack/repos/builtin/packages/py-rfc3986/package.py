# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRfc3986(PythonPackage):
    """A Python implementation of RFC 3986 including
    validation and authority parsing."""

    homepage = "https://rfc3986.readthedocs.io/"
    pypi = "rfc3986/rfc3986-1.4.0.tar.gz"
    git = "https://github.com/python-hyper/rfc3986.git"

    license("Apache-2.0")

    version("2.0.0", sha256="97aacf9dbd4bfd829baad6e6309fa6573aaf1be3f6fa735c8ab05e46cecb261c")
    version("1.4.0", sha256="112398da31a3344dc25dbf477d8df6cb34f9278a94fee2625d89e4514be8bb9d")

    variant("idna2008", default=False, description="Enable idna2008 Functionality")

    depends_on("py-setuptools", type="build")

    depends_on("py-idna", when="+idna2008")

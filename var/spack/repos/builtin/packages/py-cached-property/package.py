# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachedProperty(PythonPackage):
    """A decorator for caching properties in classes."""

    pypi = "cached-property/cached-property-1.5.1.tar.gz"

    license("BSD-3-Clause")

    version("1.5.2", sha256="9fa5755838eecbb2d234c3aa390bd80fbd3ac6b6869109bfc1b499f7bd89a130")
    version("1.5.1", sha256="9217a59f14a5682da7c4b8829deadbfc194ac22e9908ccf7c8820234e80a1504")

    depends_on("py-setuptools", type="build")

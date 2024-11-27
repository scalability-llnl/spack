# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTypesPkgResources(PythonPackage):
    """Typing stubs for pkg_resources"""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-pkg-resources/types-pkg_resources-0.1.3.tar.gz"

    version("0.1.3", sha256="834a9b8d3dbea343562fd99d5d3359a726f6bf9d3733bccd2b4f3096fbab9dae")

    depends_on("py-setuptools", type="build")

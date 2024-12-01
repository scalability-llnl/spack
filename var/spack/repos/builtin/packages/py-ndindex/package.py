# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNdindex(PythonPackage):
    """A Python library for manipulating indices of ndarrays."""

    homepage = "https://quansight-labs.github.io/ndindex/"
    pypi = "ndindex/ndindex-1.7.tar.gz"

    license("MIT")

    version("1.7", sha256="bf9bd0b76eeada1c8275e04091f8291869ed2b373b7af48e56faf7579fd2efd2")

    depends_on("py-setuptools", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLazyProperty(PythonPackage):
    """A package for making properties lazy"""

    homepage = "https://github.com/jackmaney/lazy-property"
    url = "https://github.com/jackmaney/lazy-property/archive/0.0.1.tar.gz"

    license("MIT")

    version("0.0.1", sha256="2cde89dc6f06366b3ab2423da65c469e1fe8b19f52bbd264698d1cdfdb1ef102")
    version("0.0.0", sha256="f43bea2619656eda1f80e5c781f771fee191ac3dba225f0583852be8f6d03c3f")

    depends_on("py-setuptools", type="build")

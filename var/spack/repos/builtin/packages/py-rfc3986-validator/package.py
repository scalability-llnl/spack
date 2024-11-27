# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRfc3986Validator(PythonPackage):
    """Pure python rfc3986 validator."""

    homepage = "https://github.com/naimetti/rfc3986-validator"
    pypi = "rfc3986_validator/rfc3986_validator-0.1.1.tar.gz"

    license("MIT")

    version("0.1.1", sha256="3d44bde7921b3b9ec3ae4e3adca370438eccebc676456449b145d533b240d055")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRfc3339Validator(PythonPackage):
    """A pure python RFC3339 validator."""

    homepage = "https://github.com/naimetti/rfc3339-validator"
    pypi = "rfc3339_validator/rfc3339_validator-0.1.4.tar.gz"

    license("MIT")

    version("0.1.4", sha256="138a2abdf93304ad60530167e51d2dfb9549521a836871b88d7f4695d0022f6b")

    depends_on("py-setuptools", type="build")

    depends_on("py-six", type=("build", "run"))

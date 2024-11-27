# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCustodian(PythonPackage):
    """Custodian is a simple, robust and flexible just-in-time (JIT) job management
    framework written in Python. Using custodian, you can create wrappers that
    perform error checking, job management and error recovery. It has a simple
    plugin framework that allows you to develop specific job management workflows
    for different applications."""

    homepage = "https://github.com/materialsproject/custodian"
    pypi = "custodian/custodian-2022.5.26.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("2022.5.26", sha256="92bdafa578c75f976176492e7bf3eb83abde97f112725e2e421633fa8954c6ef")

    # From setup.py:
    depends_on("py-setuptools", type="build")
    depends_on("py-monty@2.0.6:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.15.6:", type=("build", "run"))
    depends_on("py-sentry-sdk@0.8.0:", type=("build", "run"))

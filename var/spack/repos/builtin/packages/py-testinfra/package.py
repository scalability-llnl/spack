# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestinfra(PythonPackage):
    """With Testinfra you can write unit tests in Python to test actual state
    of your servers configured by management tools like Salt, Ansible, Puppet,
    Chef and so on."""

    homepage = "https://testinfra.readthedocs.io"
    pypi = "testinfra/testinfra-1.11.1.tar.gz"

    version("1.18.0", sha256="4a0a70355b007729d78446c86bffd80bcea4ffe9adc9571f9c9779476c49153d")
    version("1.13.0", sha256="b5afa23d71ee49ad81aed104e4a0f1c02819ef791291cd308fe27aa7f3d3b01f")
    version("1.12.0", sha256="ecf6f21b71bf5f4fe531c84149bfd5175465de910a6a0bb9a42c14828be7bdc1")
    version("1.11.1", sha256="a54224c39d71fe120c1f4c88330397ddcb6f6362dc38e1ce9fd53290bccbf153")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@:3.0.1,3.0.3:", type=("build", "run"))
    depends_on("py-six@1.4:", type=("build", "run"))

    # Required for testing remote systems
    depends_on("py-paramiko", type=("build", "run"))

    # Required for parallel execution
    depends_on("py-pytest-xdist", type=("build", "run"))

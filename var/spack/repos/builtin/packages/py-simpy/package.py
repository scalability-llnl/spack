# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySimpy(PythonPackage):
    """SimPy is a process-based discrete-event simulation framework based on standard Python."""

    homepage = "https://simpy.readthedocs.io/"
    pypi = "simpy/simpy-4.0.2.tar.gz"

    version("4.1.1", sha256="06d0750a7884b11e0e8e20ce0bc7c6d4ed5f1743d456695340d13fdff95001a6")
    version("4.0.2", sha256="6d8adc0229df6b02fb7e26dcd1338703b4f4f63f167a5ac2a7213cb80aba4484")

    depends_on("py-setuptools@42:", type="build", when="@4.0.2")
    depends_on("py-setuptools@64:", type="build", when="@4.1.1:")
    depends_on("py-setuptools-scm@3.4:+toml", type="build", when="@4.0.2")
    depends_on("py-setuptools-scm@8.0:+toml", type="build", when="@4.1.1:")

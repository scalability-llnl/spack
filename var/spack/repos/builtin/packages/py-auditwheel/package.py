# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAuditwheel(PythonPackage):
    """Auditing and relabeling of PEP 600 manylinux_x_y, PEP 513 manylinux1,
    PEP 571 manylinux2010 and PEP 599 manylinux2014 Linux wheels."""

    homepage = "https://github.com/pypa/auditwheel"
    pypi = "auditwheel/auditwheel-5.1.2.tar.gz"

    license("MIT")

    version("5.1.2", sha256="3ee5830014931ea84af5cd065c637b6614efa03d9b88bd8fbfc924e7ed01d6ba")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools-scm@6.2:", type="build")
    depends_on("py-pyelftools@0.24:", type=("build", "run"))
    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))

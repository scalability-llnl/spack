# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDistro(PythonPackage):
    """Distro - an OS platform information API."""

    homepage = "https://github.com/nir0s/distro"
    pypi = "distro/distro-1.5.0.tar.gz"

    license("Apache-2.0")

    version("1.8.0", sha256="02e111d1dc6a50abb8eed6bf31c3e48ed8b0830d1ea2a1b78c61765c2513fdd8")
    version("1.7.0", sha256="151aeccf60c216402932b52e40ee477a939f8d58898927378a02abbe852c1c39")
    version("1.6.0", sha256="83f5e5a09f9c5f68f60173de572930effbcc0287bb84fdc4426cb4168c088424")
    version("1.5.0", sha256="0e58756ae38fbd8fc3020d54badb8eae17c5b9dcbed388b17bb55b8a5928df92")

    depends_on("py-setuptools", type="build")

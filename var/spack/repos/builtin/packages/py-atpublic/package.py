# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAtpublic(PythonPackage):
    """This library provides two very simple decorators that document
    the publicness of the names in your module."""

    homepage = "https://public.readthedocs.io"
    pypi = "atpublic/atpublic-2.1.2.tar.gz"

    license("Apache-2.0")

    version("2.1.2", sha256="82a2f2c0343ac67913f67cdee8fa4da294a4d6b863111527a459c8e4d1a646c8")
    version("2.1.1", sha256="fa1d48bcb85bbed90f6ffee6936578f65ff0e93aa607397bd88eaeb408bd96d8")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))

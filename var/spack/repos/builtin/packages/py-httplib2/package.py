# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttplib2(PythonPackage):
    """A comprehensive HTTP client library."""

    homepage = "https://github.com/httplib2/httplib2"
    pypi = "httplib2/httplib2-0.13.1.tar.gz"

    license("MIT")

    version("0.22.0", sha256="d7a10bc5ef5ab08322488bde8c726eeee5c8618723fdb399597ec58f3d82df81")
    version("0.20.4", sha256="58a98e45b4b1a48273073f905d2961666ecf0fbac4250ea5b47aef259eb5c585")
    version("0.18.0", sha256="b0e1f3ed76c97380fe2485bc47f25235453b40ef33ca5921bb2897e257a49c4c")
    version("0.13.1", sha256="6901c8c0ffcf721f9ce270ad86da37bc2b4d32b8802d4a9cec38274898a64044")

    depends_on("py-setuptools@40.8.0:", when="@0.18.1:", type="build")
    depends_on("py-setuptools", type="build")

    depends_on("py-pyparsing@2.4.2:3", when="@0.19:", type=("build", "run"))
    conflicts("^py-pyparsing@3.0.1:3.0.3", when="@0.19:")

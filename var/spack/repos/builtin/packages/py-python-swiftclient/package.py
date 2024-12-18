# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonSwiftclient(PythonPackage):
    """This is a python client for the Swift API."""

    homepage = "https://docs.openstack.org/python-swiftclient"
    pypi = "python-swiftclient/python-swiftclient-3.9.0.tar.gz"

    maintainers("ajkotobi")

    version("4.6.0", sha256="d4d18540413893fc16ad87791d740f823f763435e8212e68eb53d60da2638233")
    version("3.12.0", sha256="313b444a14d0f9b628cbf3e8c52f2c4271658f9e8a33d4222851c2e4f0f7b7a0")
    version("3.11.1", sha256="06919d59676d3e215f4da4f3f930d71880dda3528289842b25199509df712411")
    version("3.10.0", sha256="66227eaf29a691c70675fb9982022980b92797c273dd5e6dc7e680425e9a3634")
    version("3.9.0", sha256="4f2097492e4c76e948882fc859bfa033ade09bed72f8e6b328e34a3467d9a377")
    version("3.8.1", sha256="3a013303643f77a99befa05582dfb93671e1fba1aed9f4a517418129700aedb8")
    version("3.8.0", sha256="107a9d5356663365a9f7c0b3a2b55da97a0a9ba7f10da2319b3972481510f33d")
    version("3.7.1", sha256="06bda5a6f81ea132e5cb52d0eb0616a0ab0958b4ec0d1cb7f850f04bf178852f")

    variant("keystone", default=False, description="Enable keystone authentication")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@4:")
    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build")

    depends_on("py-requests@1.1.0:", type=("build", "run"))
    depends_on("py-requests@2.4.0:", type=("build", "run"), when="@4:")

    depends_on("py-python-keystoneclient@0.7.0:", when="+keystone", type=("build", "run"))

    depends_on("py-six@1.9:", type=("build", "run"), when="@:3")

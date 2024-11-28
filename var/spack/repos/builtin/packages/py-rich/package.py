# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRich(PythonPackage):
    """Rich is a Python library for rich text and beautiful formatting
    in the terminal.
    """

    homepage = "https://github.com/willmcgugan/rich"
    pypi = "rich/rich-9.4.0.tar.gz"

    license("MIT")

    version("13.7.1", sha256="9be308cb1fe2f1f57d67ce99e95af38a1e2bc71ad9813b0e247cf7ffbcc3a432")
    version("13.4.2", sha256="d653d6bccede5844304c605d5aac802c7cf9621efd700b46c7ec2b51ea914898")
    version("12.6.0", sha256="ba3a3775974105c221d31141f2c116f4fd65c5ceb0698657a11e9f295ec93fd0")
    version("12.5.1", sha256="63a5c5ce3673d3d5fbbf23cd87e11ab84b6b451436f1b7f19ec54b6bc36ed7ca")
    version("10.14.0", sha256="8bfe4546d56b4131298d3a9e571a0742de342f1593770bd0d4707299f772a0af")
    version("10.9.0", sha256="ba285f1c519519490034284e6a9d2e6e3f16dc7690f2de3d9140737d81304d22")
    version("10.0.0", sha256="4674bd3056a72bb282ad581e3f8092dc110cdcc456b5ba76e34965cb85a69724")
    version("9.9.0", sha256="0bd8f42c3a03b7ef5e311d5e37f47bea9d268f541981c169072be5869c007957")
    version("9.8.2", sha256="c0d5903b463f015b254d6f52da82af3821d266fe516ae05fdc266e6abba5c3a8")
    version("9.8.1", sha256="0ec853f882613e75a5e46d545ddaa48cad235c616eaeb094792012fe22e8b2c6")
    version("9.8.0", sha256="c91c2587dba9aa8dd30c5f090e700f54433ccd73e209f4737e10385c4c1cbf19")
    version("9.7.0", sha256="25583ce533afae71de086ca97cf0aa883a5e1a220dfcc6049a2809a74bc79ca0")
    version("9.6.2", sha256="b6a7f9ef1a35c248498952d3454fb4f88de415dd989f97c3e5c5e2235d66e3a5")
    version("9.6.1", sha256="5ac9f4f7f6b0e32e7e412de127f15b94144e22c9a7896551474d640143bbaa7b")
    version("9.6.0", sha256="ae7f5f24fc90c76ccb54883f4bd633cbd146e0bbe3e070275ca97038ce53cf2f")
    version("9.5.1", sha256="8b937e2d2c4ff9dcfda8a5910a8cd384bd30f50ec92346d616f62065c662df5f")
    version("9.5.0", sha256="a65a9d003cb6e87e6fa5d1b53bff6f43a8d7475524c58873acdbf5bba0683fa3")
    version("9.4.0", sha256="bde23a1761373fed2802502ff98292c5d735a5389ed96f4fe1be5fb4c2cde8ea")

    depends_on("python@3.7:", when="@13:", type=("build", "run"))
    depends_on("python@3.6.3:3", when="@12.2.1:12", type=("build", "run"))
    depends_on("python@3.6.2:3", when="@10.14.0:12", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")

    depends_on("py-typing-extensions@4", when="@12.2: ^python@:3.8", type=("build", "run"))
    depends_on(
        "py-typing-extensions@3.7.4:4", when="@10.14:12.1 ^python@:3.7", type=("build", "run")
    )
    depends_on("py-typing-extensions@3.7.4:3", when="@:10.13", type=("build", "run"))
    depends_on("py-pygments@2.13:2", when="@13.3.2:", type=("build", "run"))
    depends_on("py-pygments@2.6:2", when="@:13.2", type=("build", "run"))
    depends_on("py-markdown-it-py@2.2:", when="@13.3.2:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-commonmark@0.9.0:0.9", when="@:13.1", type=("build", "run"))
    depends_on("py-colorama@0.4.0:0.4", when="@:10.14.0", type=("build", "run"))

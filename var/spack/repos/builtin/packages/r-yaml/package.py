# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RYaml(RPackage):
    """Methods to Convert R Data to YAML and Back.

    Implements the 'libyaml' 'YAML' 1.1 parser and emitter
    (<https://pyyaml.org/wiki/LibYAML>) for R."""

    cran = "yaml"

    license("BSD-3-Clause")

    version("2.3.10", sha256="e236d42d366e361d4855aa4f520260debd53a31e4786442b94770b045da02a6d")
    version("2.3.7", sha256="d20cb219e0f9c48aba02f132f81cfa9ecda5e22c925e36726840218ed56680ab")
    version("2.3.6", sha256="5dd19d8d6654ef2e4ccd6216ce8e96ca5185ae6143f95194955f6908a6e1ba26")
    version("2.3.5", sha256="3edf6c0554a0e184a25e8bec5721a2e66b4ab0dceb3737428e22705e52eb5140")
    version("2.2.2", sha256="a5dc6aba2719eb4422bdd7d3a7b2223bbb00e4470fa234d8c5b3a6835d99f730")
    version("2.2.1", sha256="1115b7bc2a397fa724956eec916df5160c600c99a3be186d21558dd38d782783")
    version("2.2.0", sha256="55bcac87eca360ab5904914fcff473a6981a1f5e6d2215d2634344d0ac30c546")
    version("2.1.19", sha256="e5db035693ac765e4b5fe1fc2e9711f8ca73e398e3f2bf27cc60def59ccd7f11")
    version("2.1.14", sha256="41a559846f6d44cc2dbcb3fc0becbc50d2766d3dc2aad7cfb97c1f9759ec0875")
    version("2.1.13", sha256="26f69aa2008bcacf3b2f95ef82a4667eaec2f2da8487646f71f1e2635d2d7fa2")

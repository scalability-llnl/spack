# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AwscliV2(AutotoolsPackage):
    """This package provides a unified command line interface to Amazon Web Services."""

    homepage = "https://docs.aws.amazon.com/cli"
    url = "https://github.com/aws/aws-cli/archive/refs/tags/2.13.22.tar.gz"

    maintainers("climbfuji")

    version("2.13.22", sha256="dd731a2ba5973f3219f24c8b332a223a29d959493c8a8e93746d65877d02afc1")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-flit-core@3.7.1:3.8.0", type=("build"))
    depends_on("py-pip@22:23", type=("build"))
    depends_on("py-colorama@0.2.5:0.4.6")
    depends_on("py-docutils@0.10:0.19")
    depends_on("py-cryptography@3.3.2:40.0.1")
    depends_on("py-ruamel-yaml@0.15:0.17.21")
    depends_on("py-ruamel-yaml-clib@0.2:0.2.7")
    depends_on("py-prompt-toolkit@3.0.24:3.0.38")
    depends_on("py-distro@1.5:1.8")
    depends_on("awscrt@0.16.4:0.16.16")
    depends_on("py-python-dateutil@2.1:2")
    depends_on("py-jmespath@0.7.1:1.0")
    depends_on("py-urllib3@1.25.4:1.26")

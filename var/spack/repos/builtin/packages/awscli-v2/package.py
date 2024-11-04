# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AwscliV2(PythonPackage):
    """This package provides a unified command line interface to Amazon Web Services."""

    homepage = "https://docs.aws.amazon.com/cli"
    url = "https://github.com/aws/aws-cli/archive/refs/tags/2.13.22.tar.gz"
    list_url = "https://github.com/aws/aws-cli/tags"

    maintainers("climbfuji", "teaguesterling")

    version("2.15.53", sha256="a4f5fd4e09b8f2fb3d2049d0610c7b0993f9aafaf427f299439f05643b25eb4b")
    version("2.13.22", sha256="dd731a2ba5973f3219f24c8b332a223a29d959493c8a8e93746d65877d02afc1")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:")
        depends_on("py-flit-core@3.7.1:3.8.0")
        depends_on("py-colorama@0.2.5:0.4.6")
        depends_on("py-docutils@0.10:0.19")
        # Remove upper bound to enable Python 3.12 support
        # depends_on("py-cryptography@3.3.2:40.0.1")
        depends_on("py-cryptography@3.3.2:")
        depends_on("py-ruamel-yaml@0.15:0.17.21")
        depends_on("py-ruamel-yaml-clib@0.2:0.2.7", when="^python@:3.9")
        depends_on("py-prompt-toolkit@3.0.24:3.0.38")
        depends_on("py-distro@1.5:1.8")
        depends_on("py-awscrt@0.16.4:0.16.16", when="@2.13")
        depends_on("py-awscrt@0.19.18:0.19.19", when="@2.15")
        depends_on("py-python-dateutil@2.1:2.8.2")
        depends_on("py-jmespath@0.7.1:1.0")
        depends_on("py-urllib3@1.25.4:1.26")

    variant("examples", default=True, description="Install code examples")

    @run_after("install", when="~examples")
    def post_install(self):
        examples_dir = join_path(python_purelib, "awscli", "examples")
        remove_directory_contents(examples_dir)

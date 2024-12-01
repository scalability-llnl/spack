# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Kinesis(MavenPackage):
    """The Amazon Kinesis Client Library for Java (Amazon KCL) enables Java
    developers to easily consume and process data from Amazon Kinesis."""

    homepage = "https://aws.amazon.com/kinesis"
    url = "https://github.com/awslabs/amazon-kinesis-client/archive/v2.2.10.tar.gz"

    license("Apache-2.0")

    version("2.4.8", sha256="f69564aee09310e9e08864160f9b021da196c0957f2042468a0cdf74a48b2e8e")
    version("2.2.10", sha256="ab1fa33466d07c41d0bbf0d1c7d2380d6f5d2957dea040ca5fe911be83bfe9f9")
    version("2.2.9", sha256="8d743c2dae127ce7c08627e7944aad4ccf025b4d71aa5486b57469c32daf20e6")
    version("2.2.8", sha256="0753d6c84247fa58c09749ca7d258a11c658b64eb65286eff74a2115613183a8")
    version("2.2.7", sha256="1838ef2327920d1df6f41db1de55318d6935d16ddde90b6e65ec65d374993177")

    depends_on("java@8", type=("build", "run"))

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Delta(Package):
    """Delta Lake is a storage layer that brings scalable, ACID transactions
    to Apache Spark and other big-data engines."""

    homepage = "https://delta.io/"
    url = "https://github.com/delta-io/delta/archive/v0.7.0.tar.gz"

    license("MIT")

    version("2.3.0", sha256="0c0ea5edb5e8f30fc56b5ab5c8fed50db93d75b047d8241fe1b2449858d9db1c")
    version("0.7.0", sha256="1fb01e36c1cf670f201c615e5fd7df88f72c27157b7d2780d146e21b266bdb64")
    version("0.6.1", sha256="c932eaf01ead08ff30ddb13ab5ad9cd43405ed8f12d5fff49bd27c59033b80df")
    version("0.6.0", sha256="bd4a4b0f164bc6a9efc58369b3f466fa2e6ae977bd6f9cd97d83dfd27a90ba3a")
    version("0.5.0", sha256="67850f20a64a459c84d2a4ed2f3bf6aa06dbb6d0da59d1499a6e7e439c6eaf04")
    version("0.4.0", sha256="177ab0bd956a261370aea577c8847bf89541d265ce97a7e18cd6ca1a1067eb1c")

    depends_on("java@8", type=("build", "run"))

    def install(self, spec, prefix):
        bash = which("bash")
        bash("build/sbt", "compile")
        bash("build/sbt", "package")
        install_tree("target", prefix.target)

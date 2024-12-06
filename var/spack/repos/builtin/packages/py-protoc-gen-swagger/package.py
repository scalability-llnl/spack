# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProtocGenSwagger(PythonPackage):
    """A python package for swagger annotation proto files."""

    homepage = "https://github.com/universe-proton/protoc-gen-swagger"
    url = "https://github.com/universe-proton/protoc-gen-swagger/archive/refs/tags/v0.1.0.tar.gz"

    license("Apache-2.0")

    version("0.1.0", sha256="bf9593eec8e0cac31fef10bd558f2a69babbb2475c67291c1c2ca84763c73067")

    depends_on("py-setuptools", type="build")
    depends_on("py-protobuf@3:", type=("build", "run"))

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPreshed(PythonPackage):
    """preshed: Cython Hash Table for Pre-Hashed Keys."""

    homepage = "https://github.com/explosion/preshed"
    pypi = "preshed/preshed-3.0.2.tar.gz"

    license("MIT")

    version("3.0.8", sha256="6c74c70078809bfddda17be96483c41d06d717934b07cab7921011d81758b357")
    version("3.0.2", sha256="61d73468c97c1d6d5a048de0b01d5a6fd052123358aca4823cdb277e436436cb")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.28:", when="@3.0.8:", type="build")
    depends_on("py-cymem@2.0.2:2.0", type=("build", "run"))
    depends_on("py-murmurhash@0.28:1.0", type=("build", "run"))

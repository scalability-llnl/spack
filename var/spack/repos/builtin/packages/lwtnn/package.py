# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lwtnn(CMakePackage):
    """Lightweight Trained Neural Network."""

    homepage = "https://github.com/lwtnn/lwtnn"
    url = "https://github.com/lwtnn/lwtnn/archive/refs/tags/v2.12.1.tar.gz"

    maintainers("haralmha")

    license("MIT")

    version("2.13", sha256="d5c1cede00f9d9cc0a25f070f744999453aec477dae6ef02701c11543c5b9553")
    version("2.12.1", sha256="b820e698d4ed60737e646ca87a42354e8ac548403348b7f2940e8fda1c0f8203")
    version("2.10", sha256="bf84b290c44da582226344b0d5febf7fdbd1cbdee94fcc8bcac972c7355564ed")

    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.54:")
    depends_on("eigen")
    # https://github.com/lwtnn/lwtnn/issues/161
    depends_on("eigen@:3.3.99", when="@2.11:2.12")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cpprestsdk(CMakePackage):
    """The C++ REST SDK is a Microsoft project for cloud-based client-server
    communication in native code using a modern asynchronous C++ API design.
    This project aims to help C++ developers connect to and interact with
    services."""

    homepage = "https://github.com/Microsoft/cpprestsdk"
    url = "https://github.com/Microsoft/cpprestsdk/archive/v2.9.1.tar.gz"

    license("MIT")

    version(
        "2.10.16",
        git="https://github.com/Microsoft/cpprestsdk",
        branch="v2.10.16",
        submodules=True,
    )
    version("2.9.1", sha256="537358760acd782f4d2ed3a85d92247b4fc423aff9c85347dc31dbb0ab9bab16")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on(
        "boost@1.69.0: +random+chrono+locale+filesystem+system+exception+regex+thread+date_time"
    )
    depends_on("openssl")

    # Ref: https://github.com/microsoft/cpprestsdk/commit/f9f518e4ad84577eb684ad8235181e4495299af4
    # Ref: https://github.com/Microsoft/cpprestsdk/commit/6b2e0480018530b616f61d5cdc786c92ba148bb7
    # Ref: https://github.com/microsoft/cpprestsdk/commit/70c1b14f39f5d47984fdd8a31fc357ebb5a37851
    patch("Release.patch", when="@2.9.1")

    root_cmakelists_dir = "Release"

    def cmake_args(self):
        args = ["-DWERROR:BOOL=Off"]

        return args

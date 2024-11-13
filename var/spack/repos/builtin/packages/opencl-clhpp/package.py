# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *


class OpenclClhpp(CMakePackage):
    """C++ headers for OpenCL development"""

    homepage = "https://www.khronos.org/registry/OpenCL/"
    url = "https://github.com/KhronosGroup/OpenCL-CLHPP/archive/v2.0.12.tar.gz"
    maintainers("lorddavidiii")

    license("Apache-2.0")

    version("2.0.16", sha256="869456032e60787eed9fceaeaf6c6cb4452bc0ff97e0f5a271510145a1c8f4d4")
    version("2.0.15", sha256="0175806508abc699586fc9a9387e01eb37bf812ca534e3b493ff3091ec2a9246")
    version("2.0.14", sha256="c8821a7638e57a2c4052631c941af720b581edda634db6ab0b59924c958d69b6")
    version("2.0.13", sha256="8ff0d0cd94d728edd30c876db546bf13e370ee7863629b4b9b5e2ef8e130d23c")
    version("2.0.12", sha256="20b28709ce74d3602f1a946d78a2024c1f6b0ef51358b9686612669897a58719")
    version("2.0.11", sha256="ffc2ca08cf4ae90ee55f14ea3735ccc388f454f4422b69498b2e9b93a1d45181")
    version("2.0.10", sha256="fa27456295c3fa534ce824eb0314190a8b3ebd3ba4d93a0b1270fc65bf378f2b")
    version("2.0.9", sha256="ba8ac4977650d833804f208a1b0c198006c65c5eac7c83b25dc32cea6199f58c")

    depends_on("cxx", type="build")  # generated

    root_cmakelists_dir = "include"

    @run_after("install")
    def post_install(self):
        if sys.platform == "darwin":
            ln = which("ln")
            ln("-s", prefix.include.CL, prefix.include.OpenCL)

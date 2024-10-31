# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPySpy(Package):
    """A Sampling Profiler for Python."""

    homepage = "https://github.com/benfred/py-spy"
    url = "https://github.com/benfred/py-spy/archive/v0.3.8.tar.gz"

    license("MIT")

    version("0.3.8", sha256="9dbfd0ea79ef31a2966891e86cf6238ed3831938cf562e71848e07b7009cf57d")
    version("0.3.3", sha256="41454d3d9132da45c72f7574faaff65f40c757720293a277ffa5ec5a4b44f902")

    depends_on("c", type="build")  # generated

    # TODO: uses cargo to download and build dozens of dependencies.
    # Need to figure out how to manage these with Spack once we have a
    # CargoPackage base class.
    depends_on("rust", type="build")
    depends_on("unwind")
    depends_on("libunwind components=ptrace", when="^[virtuals=unwind] libunwind")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Task(CMakePackage):
    """Feature-rich console based todo list manager"""

    homepage = "https://www.taskwarrior.org"
    url = "https://taskwarrior.org/download/task-2.4.4.tar.gz"

    license("MIT")

    version("3.0.0", sha256="30f397081044f5dc2e5a0ba51609223011a23281cd9947ea718df98d149fcc83")
    version("2.6.2", sha256="b1d3a7f000cd0fd60640670064e0e001613c9e1cb2242b9b3a9066c78862cfec")
    version("2.5.1", sha256="d87bcee58106eb8a79b850e9abc153d98b79e00d50eade0d63917154984f2a15")
    version("2.4.4", sha256="7ff406414e0be480f91981831507ac255297aab33d8246f98dbfd2b1b2df8e3b")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8:", type="build")
    depends_on("gnutls")
    depends_on("uuid")
    depends_on("rust@1.64.0:", when="@3.0.0:")

    conflicts("%gcc@:4.7")

    def patch(self):
        if self.spec.satisfies("@3.0.0:"):
            # new major release adds rust to the codebase. A bug in cmake/Corrosion
            # causes release builds with the integration tests to fail.
            # See https://github.com/GothenburgBitFactory/taskwarrior/issues/3294
            filter_file('"taskchampion/integration-tests",', "", "Cargo.toml")

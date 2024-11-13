# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qtkeychain(CMakePackage):
    """Platform-independent Qt API for storing passwords securely."""

    homepage = "https://github.com/frankosterfeld/qtkeychain"
    url = "https://github.com/frankosterfeld/qtkeychain/archive/v0.9.1.tar.gz"

    license("BSD-2-Clause")

    version("0.9.1", sha256="9c2762d9d0759a65cdb80106d547db83c6e9fdea66f1973c6e9014f867c6f28e")

    depends_on("cxx", type="build")  # generated

    depends_on("qt+dbus")
    depends_on("libsecret")

    def cmake_args(self):
        args = []
        if self.spec["qt"].version.up_to(1) == Version("4"):
            args.append("-DBUILD_WITH_QT4=ON")
        return args

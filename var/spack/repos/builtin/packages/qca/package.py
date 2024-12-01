# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qca(CMakePackage):
    """Taking a hint from the similarly-named Java Cryptography Architecture,
    QCA aims to provide a straightforward and cross-platform crypto API,
    using Qt datatypes and conventions. QCA separates the API from the
    implementation, using plugins known as Providers. The advantage of
    this model is to allow applications to avoid linking to or explicitly
    depending on any particular cryptographic library. This allows one to
    easily change or upgrade crypto implementations without even needing
    to recompile the application!
    QCA should work everywhere Qt does, including Windows/Unix/MacOSX."""

    homepage = "https://userbase.kde.org/QCA"
    url = "https://github.com/KDE/qca/archive/v2.1.3.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.3.5", sha256="326346893c5ad41c160b66ff10740ff4d8a1cbcd2fe545693f9791de1e01f00b")
    version("2.3.0", sha256="39aa18f0985d82949f4dccce04af3eb8d4b6b64e0c71785786738d38d8183b0a")
    version("2.2.90", sha256="074ac753b51a6fa15503be9418f7430effe368fd31dc41567942d832e539b17e")
    version("2.2.1", sha256="c67fc0fa8ae6cb3d0ba0fbd8fca8ee8e4c5061b99f1fd685fd7d9800cef17f6b")
    version("2.1.3", sha256="a5135ffb0250a40e9c361eb10cd3fe28293f0cf4e5c69d3761481eafd7968067")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("qt@4.2:")

    depends_on("qt@:5.10.0", when="@2.1.3")

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_CXX_STANDARD=11")
        if self.spec["qt"].version.up_to(1) == Version("4"):
            args.append("-DQT4_BUILD=ON")
        return args

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qjson(CMakePackage):
    """QJson is a Qt-based library that maps JSON data to QVariant
    objects and vice versa."""

    homepage = "https://qjson.sourceforge.net/"
    url = "https://github.com/flavio/qjson/archive/0.9.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.9.0", sha256="e812617477f3c2bb990561767a4cd8b1d3803a52018d4878da302529552610d4")

    depends_on("cxx", type="build")  # generated

    depends_on("qt")

    def cmake_args(self):
        args = []
        if self.spec["qt"].version.up_to(1) == Version("4"):
            args.append("-DQT4_BUILD=ON")
        return args

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Loki(MakefilePackage):
    """Loki is a C++ library of designs, containing flexible implementations
    of common design patterns and idioms."""

    homepage = "https://loki-lib.sourceforge.net"
    url = "https://downloads.sourceforge.net/project/loki-lib/Loki/Loki%200.1.7/loki-0.1.7.tar.bz2"
    tags = ["e4s"]

    license("Apache-2.0")

    version("0.1.7", sha256="07553754f6be2738559947db69b0718512665bf4a34015fa3a875b6eb1111198")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            if self.spec.satisfies("%oneapi@2023.0.0:"):
                flags.append("-Wno-error=dynamic-exception-spec")
            if self.spec.satisfies("@0.1.7 %gcc@11:"):
                flags.append("-std=c++14")
        return (flags, None, None)

    def build(self, spec, prefix):
        if spec.satisfies("+shared"):
            make("-C", "src", "build-shared")
        else:
            make("-C", "src", "build-static")

    def install(self, spec, prefix):
        make("-C", "include", "install", "prefix={0}".format(prefix))
        if spec.satisfies("+shared"):
            make("-C", "src", "install-shared", "prefix={0}".format(prefix))
        else:
            make("-C", "src", "install-static", "prefix={0}".format(prefix))

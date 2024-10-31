# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Libkml(CMakePackage):
    """Reference implementation of OGC KML 2.2."""

    # NOTE: The original libkml repo is https://github.com/google/libkml,
    # but this project is dead. See https://github.com/google/libkml/issues/4

    homepage = "https://github.com/libkml/libkml"
    url = "https://github.com/libkml/libkml/archive/1.3.0.tar.gz"

    license("BSD-3-Clause")

    version("1.3.0", sha256="8892439e5570091965aaffe30b08631fdf7ca7f81f6495b4648f0950d7ea7963")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("java", default=False, description="Build java bindings")
    variant("python", default=False, description="Build python bindings")

    extends("openjdk", when="+java")
    extends("python", when="+python")

    # See DEPENDENCIES
    depends_on("cmake@2.8:", type="build")
    # FIXME: Can the maintainers confirm if this is a required dependency
    depends_on("boost@1.44.0:")
    depends_on(Boost.with_default_variants)
    depends_on("expat@2.1.0:")
    depends_on("minizip@1.2.8:")
    depends_on("uriparser")
    depends_on("zlib-api")
    conflicts("^zlib@:1.2.7")
    depends_on("googletest@1.7.0:", type="link")
    depends_on("swig", when="+java", type="build")
    depends_on("swig", when="+python", type="build")

    @property
    def libs(self):
        return find_libraries("libkmlbase", root=self.prefix, recursive=True)

    def cmake_args(self):
        spec = self.spec

        args = []

        if spec.satisfies("+java"):
            args.append("-DWITH_JAVA:BOOL=ON")
        else:
            args.append("-DWITH_JAVA:BOOL=OFF")

        if spec.satisfies("+python"):
            args.append("-DWITH_PYTHON:BOOL=ON")
        else:
            args.append("-DWITH_PYTHON:BOOL=OFF")

        if self.run_tests:
            args.append("-DBUILD_TESTING:BOOL=ON")
            args.append("-DGTEST_INCLUDE_DIR:PATH={0}".format(spec["googletest"].prefix.include))
        else:
            args.append("-DBUILD_TESTING:BOOL=OFF")

        return args

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack.package import *


class AttributesFoo(BundlePackage):
    version("1.0")

    provides("bar")
    provides("baz")

    def install(self, spec, prefix):
        lib_suffix = ".so"
        if sys.platform == "win32":
            lib_suffix = ".dll"
        elif sys.platform == "darwin":
            lib_suffix = ".dylib"
        mkdirp(prefix.include)
        touch(prefix.include.join("foo.h"))
        mkdirp(prefix.include.bar)
        touch(prefix.include.bar.join("bar.h"))
        mkdirp(prefix.lib64)
        touch(prefix.lib64.join("libFoo" + lib_suffix))
        touch(prefix.lib64.join("libFooBar" + lib_suffix))
        mkdirp(prefix.baz.include.baz)
        touch(prefix.baz.include.baz.join("baz.h"))
        mkdirp(prefix.baz.lib)
        touch(prefix.baz.lib.join("libFooBaz" + lib_suffix))

    # Headers provided by Foo
    @property
    def headers(self):
        return find_headers("foo", root=self.home.include, recursive=False)

    # Libraries provided by Foo
    @property
    def libs(self):
        return find_libraries("libFoo", root=self.home, recursive=True)

    # Header provided by the bar virutal package
    @property
    def bar_headers(self):
        return find_headers("bar/bar", root=self.home.include, recursive=False)

    # Libary provided by the bar virtual package
    @property
    def bar_libs(self):
        return find_libraries("libFooBar", root=self.home, recursive=True)

    # The baz virtual package home
    @property
    def baz_home(self):
        return self.home.baz

    # Header provided by the baz virtual package
    @property
    def baz_headers(self):
        return find_headers("baz/baz", root=self.baz_home.include, recursive=False)

    # Library provided by the baz virtual package
    @property
    def baz_libs(self):
        return find_libraries("libFooBaz", root=self.baz_home, recursive=True)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CommonsLang(Package):
    """The standard Java libraries fail to provide enough methods for
    manipulation of its core classes. Apache Commons Lang provides these
    extra methods.

    Lang provides a host of helper utilities for the java.lang API, notably
    String manipulation methods, basic numerical methods, object reflection,
    concurrency, creation and serialization and System properties. Additionally
    it contains basic enhancements to java.util.Date and a series of utilities
    dedicated to help with building methods, such as hashCode, toString and
    equals."""

    homepage = "https://commons.apache.org/proper/commons-lang/"
    url = "https://archive.apache.org/dist/commons/lang/binaries/commons-lang-2.6-bin.tar.gz"

    license("Apache-2.0")

    version("2.6", sha256="ff6a244bb71a9a1c859e81cb744d0ce698c20e04f13a7ef7dbffb99c8122752c")
    version("2.4", sha256="00e6b3174e31196d726c14302c8e7e9ba9b8409d57a8a9821c7648beeda31c5e")

    extends("openjdk")
    depends_on("java@2:", type="run")

    def install(self, spec, prefix):
        install("commons-lang-{0}.jar".format(self.version), prefix)

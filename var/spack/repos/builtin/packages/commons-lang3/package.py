# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CommonsLang3(Package):
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
    url = "https://archive.apache.org/dist/commons/lang/binaries/commons-lang3-3.7-bin.tar.gz"

    license("Apache-2.0")

    version("3.14.0", sha256="317c3e3fcd5fcca3781a7996ff1e0c50c13244ee961e94e5f6f6d84b84733b16")
    version("3.12.0", sha256="33012465dfcb7f790aca333e09ebf105e2a5fb95c2c638b3df790d3efa908e28")
    version("3.7", sha256="94dc8289ce90b77b507d9257784d9a43b402786de40c164f6e3990e221a2a4d2")

    extends("openjdk")
    depends_on("java@7:", type="run")

    def install(self, spec, prefix):
        install(f"commons-lang3-{self.version}.jar", prefix)

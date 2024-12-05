# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nspr(AutotoolsPackage):
    """Netscape Portable Runtime (NSPR) provides a platform-neutral API
    for system level and libc-like functions."""

    homepage = (
        "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS/Reference/NSPR_functions"
    )
    url = "https://ftp.mozilla.org/pub/nspr/releases/v4.13.1/src/nspr-4.13.1.tar.gz"

    license("MPL-2.0")

    version("4.35", sha256="7ea3297ea5969b5d25a5dd8d47f2443cda88e9ee746301f6e1e1426f8a6abc8f")
    version("4.32", sha256="bb6bf4f534b9559cf123dcdc6f9cd8167de950314a90a88b2a329c16836e7f6c")
    version("4.31", sha256="5729da87d5fbf1584b72840751e0c6f329b5d541850cacd1b61652c95015abc8")
    version("4.13.1", sha256="5e4c1751339a76e7c772c0c04747488d7f8c98980b434dc846977e43117833ab")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("perl", type="build")

    configure_directory = "nspr"

    def configure_args(self):
        return [
            "--with-mozilla",
            "--enable-64bit",  # without this, fails when 32-bit glibc not found
            "--enable-optimize",
        ]

    @property
    def headers(self):
        headers = find_headers("*", self.prefix.include, recursive=True)
        headers.directories = [self.prefix.include.nspr]
        return headers

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Clamav(AutotoolsPackage):
    """Open source antivirus engine for detecting trojans,
    viruses, malware & other malicious threats."""

    homepage = "https://www.clamav.net/"
    url = "https://www.clamav.net/downloads/production/clamav-0.101.2.tar.gz"

    license("GPL-2.0-only")

    version("0.101.2", sha256="0a12ebdf6ff7a74c0bde2bdc2b55cae33449e6dd953ec90824a9e01291277634")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("json-c")
    depends_on("openssl")
    depends_on("pcre")
    depends_on("yara")
    depends_on("zlib-api")
    depends_on("bzip2")
    depends_on("curl", type="link")

    def configure_args(self):
        spec = self.spec
        args = [
            "--enable-llvm=no",
            "--with-libjson=%s" % spec["json-c"].prefix,
            "--with-openssl=%s" % spec["openssl"].prefix,
            "--with-pcre=%s" % spec["pcre"].prefix,
            "--with-zlib=%s" % spec["zlib-api"].prefix,
            "--with-bzip2=%s" % spec["bzip2"].prefix,
        ]
        return args

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Zip(MakefilePackage):
    """Zip is a compression and file packaging/archive utility."""

    homepage = "https://www.info-zip.org/Zip.html"
    url = "https://downloads.sourceforge.net/infozip/zip30.tar.gz"

    license("Info-ZIP")

    version("3.0", sha256="f0e8bb1f9b7eb0b01285495a2699df3a4b766784c1765a8f1aeedf63c0806369")

    depends_on("c", type="build")  # generated

    depends_on("bzip2")

    # Upstream is unmaintained, get patches from:
    # https://deb.debian.org/debian/pool/main/z/zip/zip_3.0-11.debian.tar.xz
    patch("01-typo-it-is-transferring-not-transfering.patch")
    patch("02-typo-it-is-privileges-not-priviliges.patch")
    patch("03-manpages-in-section-1-not-in-section-1l.patch")
    patch("04-do-not-set-unwanted-cflags.patch")
    patch("05-typo-it-is-preceding-not-preceeding.patch")
    patch("06-stack-markings-to-avoid-executable-stack.patch")
    patch("07-fclose-in-file-not-fclose-x.patch")
    patch("08-hardening-build-fix-1.patch")
    patch("09-hardening-build-fix-2.patch")
    patch("10-remove-build-date.patch")
    patch("11-typo-it-is-ambiguities-not-amgibuities.patch")

    # Configure and header changes needed for comatibility with strict gcc14+
    # these are not from the debian branch
    patch("12-gcc14-no-implicit-declarations-fix.patch", when="%gcc@14:")

    executables = ["^zip$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"This is Zip (\S+)", output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        return f"http://downloads.sourceforge.net/infozip/zip{version.joined}.tar.gz"

    def build(self, spec, prefix):
        make("-f", "unix/Makefile", "CC=" + spack_cc, "generic")

    def install(self, spec, prefix):
        make("-f", "unix/Makefile", "prefix=" + prefix, "install")

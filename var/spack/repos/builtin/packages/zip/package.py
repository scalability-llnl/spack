# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Zip(MakefilePackage):
    """Zip is a compression and file packaging/archive utility."""

    homepage = 'https://www.info-zip.org/Zip.html'
    url      = 'https://downloads.sourceforge.net/infozip/zip30.tar.gz'

    version('3.0', sha256='f0e8bb1f9b7eb0b01285495a2699df3a4b766784c1765a8f1aeedf63c0806369')

    depends_on('bzip2')

    # Upstream is unmaintained, get patches from:
    # https://deb.debian.org/debian/pool/main/z/zip/zip_3.0-11.debian.tar.xz
    patch('01-typo-it-is-transferring-not-transfering.patch')
    patch('02-typo-it-is-privileges-not-priviliges.patch')
    patch('03-manpages-in-section-1-not-in-section-1l.patch')
    patch('04-do-not-set-unwanted-cflags.patch')
    patch('05-typo-it-is-preceding-not-preceeding.patch')
    patch('06-stack-markings-to-avoid-executable-stack.patch')
    patch('07-fclose-in-file-not-fclose-x.patch')
    patch('08-hardening-build-fix-1.patch')
    patch('09-hardening-build-fix-2.patch')
    patch('10-remove-build-date.patch')

    def url_for_version(self, version):
        return 'http://downloads.sourceforge.net/infozip/zip{0}.tar.gz'.format(version.joined)

    def build(self, spec, prefix):
        make('-f', 'unix/Makefile', 'CC=' + spack_cc, 'generic')

    def install(self, spec, prefix):
        make('-f', 'unix/Makefile', 'prefix=' + prefix, 'install')

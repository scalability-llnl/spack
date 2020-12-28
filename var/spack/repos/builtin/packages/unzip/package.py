# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unzip(MakefilePackage):
    """Unzip is a compression and file packaging/archive utility."""

    homepage = 'http://www.info-zip.org/Zip.html'
    url      = 'http://downloads.sourceforge.net/infozip/unzip60.tar.gz'

    version('6.0', sha256='036d96991646d0449ed0aa952e4fbe21b476ce994abc276e49d30e686708bd37')

    # The Cray cc wrapper doesn't handle the '-s' flag (strip) cleanly.
    @when('platform=cray')
    def patch(self):
        filter_file(r'^LFLAGS2=.*', 'LFLAGS2=', join_path('unix', 'configure'))

    make_args = [
        '-f', join_path('unix', 'Makefile'),
        "LOC=-DLARGE_FILE_SUPPORT"
    ]

    @property
    def build_targets(self):
        target = "macosx" if "platform=darwin" in self.spec else "generic"
        return self.make_args + [target]

    def url_for_version(self, version):
        return 'http://downloads.sourceforge.net/infozip/unzip{0}.tar.gz'.format(version.joined)

    @property
    def install_targets(self):
        return self.make_args + ['prefix={0}'.format(self.prefix), 'install']

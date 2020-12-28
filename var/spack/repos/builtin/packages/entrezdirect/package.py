# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Entrezdirect(Package):
    """Entrez Direct (EDirect) provides access to the NCBI's suite of
       interconnected databases (publication, sequence, structure,
       gene, variation, expression, etc.) from a UNIX terminal window."""

    homepage = "https://www.ncbi.nlm.nih.gov/books/NBK179288/"

    version('10.7.20190114', sha256='4152749e6a3aac71a64e9367527428714ed16cf1fb6c7eff1298cca9ef144c0d')

    depends_on('perl', type='run')
    depends_on('perl-html-parser', type='run')
    depends_on('perl-libwww-perl', type='run')
    depends_on('perl-lwp-protocol-https', type='run')
    depends_on('perl-http-message', type='run')
    depends_on('perl-xml-simple', type='run')

    def url_for_version(self, ver):
        pfx = 'ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/versions/'
        return pfx + '{0}/edirect-{0}.tar.gz'.format(ver.dotted)

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)

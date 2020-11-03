# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re


class Krb5(AutotoolsPackage):
    """Network authentication protocol"""

    homepage   = "https://kerberos.org"
    url        = "https://kerberos.org/dist/krb5/1.16/krb5-1.16.1.tar.gz"
    list_url   = "https://kerberos.org/dist/krb5/"
    list_depth = 1

    version('1.18.2', sha256='c6e4c9ec1a98141c3f5d66ddf1a135549050c9fab4e9a4620ee9b22085873ae0')
    version('1.18.1', sha256='02a4e700f10936f937cd1a4c303cab8687a11abecc6107bd4b706b9329cd5400')
    version('1.18',   sha256='73913934d711dcf9d5f5605803578edb44b9a11786df3c1b2711f4e1752f2c88')
    version('1.17.1', sha256='3706d7ec2eaa773e0e32d3a87bf742ebaecae7d064e190443a3acddfd8afb181')
    version('1.17',   sha256='5a6e2284a53de5702d3dc2be3b9339c963f9b5397d3fbbc53beb249380a781f5')
    version('1.16.3', sha256='e40499df7c6dbef0cf9b11870a0e167cde827737d8b2c06a9436334f08ab9b0d')
    version('1.16.2', sha256='9f721e1fe593c219174740c71de514c7228a97d23eb7be7597b2ae14e487f027')
    version('1.16.1', sha256='214ffe394e3ad0c730564074ec44f1da119159d94281bbec541dc29168d21117')

    depends_on('bison', type='build')
    depends_on('openssl')

    configure_directory = 'src'
    build_directory = 'src'

    executables = ['^krb5-config$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'Kerberos 5 release\s+(\S+)', output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        url = 'https://kerberos.org/dist/krb5/{0}/krb5-{1}.tar.gz'
        return url.format(version.up_to(2), version)

    def patch(self):
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/krb5.rb
        # https://krbdev.mit.edu/rt/Ticket/Display.html?id=8928
        filter_file(
            'void foo1() __attribute__((constructor));',
            '#include <unistd.h>\nvoid foo1() __attribute__((constructor));',
            join_path(self.configure_directory, 'configure'),
            string=True)

    def configure_args(self):
        return ['--without-system-verto']

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsodium(AutotoolsPackage):
    """Sodium is a modern, easy-to-use software library for encryption,
    decryption, signatures, password hashing and more."""
    homepage = "https://download.libsodium.org/doc/"
    url      = "https://download.libsodium.org/libsodium/releases/libsodium-1.0.13.tar.gz"
    list_url = "https://download.libsodium.org/libsodium/releases/old"

    version('1.0.18', sha256='6f504490b342a4f8a4c4a02fc9b866cbef8622d5df4e5452b46be121e46636c1')
    version('1.0.17', sha256='0cc3dae33e642cc187b5ceb467e0ad0e1b51dcba577de1190e9ffa17766ac2b1')
    version('1.0.16', sha256='eeadc7e1e1bcef09680fb4837d448fbdf57224978f865ac1c16745868fbd0533')
    version('1.0.15', sha256='fb6a9e879a2f674592e4328c5d9f79f082405ee4bb05cb6e679b90afe9e178f4')
    version('1.0.13', sha256='9c13accb1a9e59ab3affde0e60ef9a2149ed4d6e8f99c93c7a5b97499ee323fd')
    version('1.0.3', sha256='cbcfc63cc90c05d18a20f229a62c7e7054a73731d0aa858c0517152c549b1288')
    version('1.0.2', sha256='961d8f10047f545ae658bcc73b8ab0bf2c312ac945968dd579d87c768e5baa19')
    version('1.0.1', sha256='c3090887a4ef9e2d63af1c1e77f5d5a0656fadb5105ebb9fb66a302210cb3af5')
    version('1.0.0', sha256='ced1fe3d2066953fea94f307a92f8ae41bf0643739a44309cbe43aa881dbc9a5')
    version('0.7.1', sha256='ef46bbb5bac263ef6d3fc00ccc11d4690aea83643412919fe15369b9870280a7')

    def url_for_version(self, version):
        url = 'https://download.libsodium.org/libsodium/releases/'
        if version < Version('1.0.4'):
            url += 'old/unsupported/'
        elif version < Version('1.0.16'):
            url += 'old/'
        return url + 'libsodium-{0}.tar.gz'.format(version)

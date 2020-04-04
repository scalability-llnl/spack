# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Skopeo(MakefilePackage):
    """skopeo is a command line utility that performs various operations on
    container images and image repositories."""

    homepage = "https://github.com/containers/skopeo"
    url      = "https://github.com/containers/skopeo/archive/v0.1.39.tar.gz"

    version('0.1.40', sha256='ee1e33245938fcb622f5864fac860e2d8bfa2fa907af4b5ffc3704ed0db46bbf')
    version('0.1.39', sha256='e9d70f7f7b891675a816f06a22df0490285ad20eefbd91f5da69ca12f56c29f2')
    version('0.1.38', sha256='104ceb9c582dc5c3a49dd1752c4c326bba03f2f801596f089372e831f48ed705')

    depends_on('go@1.11:')
    depends_on('go-md2man', type='build')
    depends_on('gpgme')
    depends_on('libassuan')
    depends_on('libgpg-error')
    depends_on('lvm2')

    def edit(self, spec, prefix):
        grep = which('grep')
        files = grep('-lR', '/etc/containers/', 'vendor', output=str,
                     env={'PATH': '/usr/bin:/bin:/usr/sbin:/sbin'})

        for f in files.splitlines():
            edit = FileFilter(f)
            edit.filter('/etc/containers/', '{0}/etc/containers/'.
                        format(prefix))

    def build(self, spec, prefix):
        make('binary-local')

    def install(self, spec, prefix):
        make('binary-local', 'install',
             'DESTDIR={0}'.format(prefix),
             'PREFIX={0}'.format(prefix))

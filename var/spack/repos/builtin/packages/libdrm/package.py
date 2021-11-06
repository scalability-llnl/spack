# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libdrm(Package):
    """A userspace library for accessing the DRM, direct rendering manager,
    on Linux, BSD and other systems supporting the ioctl interface."""

    homepage = "https://dri.freedesktop.org/libdrm/"
    list_url = "https://dri.freedesktop.org/libdrm/"

    version('2.4.107', sha256='c554cef03b033636a975543eab363cc19081cb464595d3da1ec129f87370f888')
    version('2.4.100', sha256='6a5337c054c0c47bc16607a21efa2b622e08030be4101ef4a241c5eb05b6619b')
    version('2.4.81',  sha256='64036c5e0668fdc2b820dcc0ebab712f44fd2c2147d23dc5a6e003b19f0d3e9f')
    version('2.4.75',  sha256='a411bff814b4336c8908dcbd045cd89fdc7afedc75b795d897d462e467cbb01d')
    version('2.4.70',  sha256='73615b9c1c4852e5ce045efa19c866e8df98e396b2443bf859eea05574ecb64f')
    version('2.4.59',  sha256='ed9d03a92c2d80e6310cc350db3430620f1659ae084a07c6824cee7bc81ae8fa')
    version('2.4.33',  sha256='bd2a8fecf28616f2157ca33ede691c139cc294ed2d0c4244b62ca7d22e98e5a4')

    depends_on('pkgconfig', type='build')
    depends_on('docbook-xml', type='build')
    depends_on('docbook-xsl', type='build')
    depends_on('libpciaccess@0.10:')
    depends_on('libpthread-stubs')

    def url_for_version(self, version):
        if version <= Version('2.4.100'):
            return self.list_url + 'libdrm-%s.tar.gz' % version
        else:
            return self.list_url + 'libdrm-%s.tar.xz' % version

    def meson_args(self):
        args = []
        return args

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            args = []
            args.extend(std_meson_args)
            args.extend(self.meson_args())
            meson('..', *args)
            ninja('-v')
            if self.run_tests:
                ninja('test')
            ninja('install')

    @when('@:2.4.100')
    def configure_args(self):
        args = []
        args.append('--enable-static')
        if self.version <= Version('2.4.70'):
            # Needed to fix build for spack/spack#1740, but breaks newer
            # builds/compilers
            args.append('LIBS=-lrt')
        if self.spec.satisfies('%gcc@10.0.0:') or self.spec.satisfies('%clang@11.0.0:') or self.spec.satisfies('%aocc@2.3.0:'):
            args.append('CFLAGS=-fcommon')
        return args

    @when('@:2.4.100')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix), *self.configure_args())
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')

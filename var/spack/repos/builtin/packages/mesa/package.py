##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import distro


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "http://ftp.iij.ad.jp/pub/X11/x.org/pub/mesa/12.0.3/mesa-12.0.3.tar.gz"

    version('12.0.3', '60c5f9897ddc38b46f8144c7366e84ad')

    variant('dri', default=True, description='Enable DRI and EGL support')
    variant('osmesa', default=False, description='Enable OSMesa support')
    conflicts('+dri', '+osmesa')

    # General dependencies
    depends_on('python@2.6.4:')
    depends_on('py-mako@0.3.4:', type=('build', 'run'))
    depends_on('flex@2.5.35:', type='build')
    depends_on('bison@2.4.1:', type='build')

    # For DRI and hardware acceleration
    depends_on('libpthread-stubs')
    depends_on('libdrm')
    depends_on('openssl')
    depends_on('libxcb@1.9.3:')
    depends_on('libxshmfence@1.1:')
    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxdamage')
    depends_on('libxfixes')

    depends_on('glproto@1.4.14:', type='build')
    depends_on('dri2proto@2.6:', when='+dri', type='build')
    depends_on('dri3proto@1.0:', when='+dri', type='build')
    depends_on('presentproto@1.0:', type='build')
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('llvm', when='+osmesa', type='build')

    # adamjstewart
    # TODO: Add package for systemd, provides libudev
    # Using the system package manager to install systemd didn't work for me
    # justiceformikebrown
    # Added:
    # ~dri will disable dri on older Centos /RHEL6 servers
    # which lack newer udev
    # You must also yum install libsysfs-devel
    # https://www.mesa3d.org/osmesa.html
    # https://www.mesa3d.org/autoconf.html
    def configure_args(self):
        spec = self.spec
        version = distro.linux_distribution()[1]
        distname = distro.linux_distribution()[0]
        strversion = version.encode('utf-8')
        # centos / rhel 6
        if distname == "RedHatEnterpriseServer":
            if strversion.find('6.0:6.9') == -1:
                args = []
            else:
                args = ['--enable-sysfs']
        elif distname == "CentOS":
            if strversion.find('6.0:6.9') == -1:
                args = []
            else:
                args = ['--enable-sysfs']
        else:
            args = []

        if '~dri' in spec:
            args.extend([
                '--disable-dri',
                '--disable-egl',
                '--disable-driglx-direct',
                '--with-gallium-drivers=swrast'
            ])
        else:
            args.extend([
                '--enable-dri',
                '--enable-egl'
            ])

        if '+osmesa' in spec:
            args.extend([
                '--enable-osmesa',
                '--disable-driglx-direct',
                '--disable-dri',
                '--with-gallium-drivers=llvmpipe'
            ])
        return args

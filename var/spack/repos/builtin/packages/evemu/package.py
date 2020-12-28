# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Evemu(AutotoolsPackage):
    """The evemu library and tools are used to describe devices, record data,
    create devices and replay data from kernel evdev devices."""

    homepage = "https://github.com/freedesktop/evemu"
    url      = "https://github.com/freedesktop/evemu/archive/v2.7.0.tar.gz"

    version('2.7.0', sha256='aee1ecc2b6761134470316d97208b173adb4686dc72548b82b2c2b5d1e5dc259')
    version('2.6.0', sha256='dc2382bee4dcb6c413271d586dc11d9b4372a70fa2b66b1e53a7107f2f9f51f8')
    version('2.5.0', sha256='ab7cce32800db84ab3504789583d1be0d9b0a5f2689389691367b18cf059b09f')
    version('2.4.0', sha256='d346ec59289f588bd93fe3cfa40858c7e048660164338787da79b9ebe3256069')
    version('2.3.1', sha256='f2dd97310520bc7824adc38b69ead22c53944a666810c60a3e49592914e14e8a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('libevdev@1.2.99.902:')

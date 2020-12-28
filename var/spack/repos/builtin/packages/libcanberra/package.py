# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcanberra(AutotoolsPackage):
    """libcanberra is an implementation of the XDG Sound Theme and
    Name Specifications, for generating event sounds on free desktops,
    such as GNOME."""

    homepage = "http://0pointer.de/lennart/projects/libcanberra/"
    url      = "http://0pointer.de/lennart/projects/libcanberra/libcanberra-0.30.tar.xz"

    version('0.30', sha256='c2b671e67e0c288a69fc33dc1b6f1b534d07882c2aceed37004bf48c601afa72')

    # TODO: Add variants and dependencies for the following audio support:
    # ALSA, OSS, PulseAudio, udev, GStreamer, null, GTK3+ , tdb

    variant('gtk', default=False, description='Enable optional GTK+ support')

    depends_on('libxrender',    when='+gtk')
    depends_on('libxext',       when='+gtk')
    depends_on('libx11',        when='+gtk')
    depends_on('libxinerama',   when='+gtk')
    depends_on('libxrandr',     when='+gtk')
    depends_on('libxcursor',    when='+gtk')
    depends_on('libxcomposite', when='+gtk')
    depends_on('libxdamage',    when='+gtk')
    depends_on('libxfixes',     when='+gtk')
    depends_on('libxcb',        when='+gtk')
    depends_on('libxau',        when='+gtk')
    depends_on('gtkplus',       when='+gtk')

    depends_on('libvorbis')

    depends_on('pkgconfig', type='build')

    def configure_args(self):
        args = ['--enable-static']

        if '+gtk' in self.spec:
            args.append('--enable-gtk')
        else:
            args.append('--disable-gtk')

        return args

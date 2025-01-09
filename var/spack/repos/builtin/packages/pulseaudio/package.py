# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pulseaudio(AutotoolsPackage):
    """PulseAudio is a sound system for POSIX OSes, meaning that it is a proxy
    for your sound applications.

    PulseAudio is a sound system for POSIX OSes, meaning that it is a proxy for
    your sound applications. It allows you to do advanced operations on your
    sound data as it passes between your application and your hardware. Things
    like transferring the audio to a different machine, changing the sample
    format or channel count and mixing several sounds into one are easily
    achieved using a sound server."""

    homepage = "https://www.freedesktop.org/wiki/Software/PulseAudio/"
    url = "https://freedesktop.org/software/pulseaudio/releases/pulseaudio-13.0.tar.xz"

    license("LGPL-2.1-or-later")

    version("13.0", sha256="961b23ca1acfd28f2bc87414c27bb40e12436efcf2158d29721b1e89f3f28057")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("alsa", default=False, description="alsa support")
    variant("fftw", default=False, description="FFTW support")
    variant("gconf", default=False, description="Gconf support")
    variant("openssl", default=False, description="openSSL support (used for Airtunes/RAOP)")
    variant("x11", default=False, description="x11 support")

    depends_on("alsa-lib@1.0.19:", when="+alsa")
    depends_on("dbus@1.4.12:")
    depends_on("fftw@3:", when="+fftw")
    depends_on("gdbm")
    depends_on("gettext@0.18.1:")
    depends_on("glib")
    depends_on("gconf", when="+gconf")
    depends_on("json-c@0.11:")
    depends_on("libcap")
    depends_on("iconv")
    depends_on("libsndfile@1.0.18:")
    depends_on("libtool@2.4:", type="link")  # links to libltdl.so
    depends_on("libsm", when="+x11")
    depends_on("uuid", when="+x11")
    depends_on("libx11", when="+x11")
    depends_on("libxcb", when="+x11")
    depends_on("libxau", when="+x11")
    depends_on("libxext", when="+x11")
    depends_on("libxi", when="+x11")
    depends_on("libxtst", when="+x11")
    depends_on("openssl", when="+openssl")
    depends_on("perl-xml-parser", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("speexdsp@1.2:")
    depends_on("m4", type="build")

    def configure_args(self):
        args = [
            "--disable-systemd-daemon",
            "--disable-systemd-journal",
            "--disable-systemd-login",
            "--disable-udev",
            "--disable-waveout",
            "--enable-dbus",
            "--enable-glib2",
            "--with-database=gdbm",
            "--with-systemduserunitdir=no",
            "CPPFLAGS={0}".format(self.spec["libtool"].headers.cpp_flags),
            "LDFLAGS={0}".format(self.spec["libtool"].libs.search_flags),
        ]

        # toggle based on variants
        args += self.enable_or_disable("alsa")
        args += self.enable_or_disable("gconf")
        args += self.enable_or_disable("openssl")
        args += self.enable_or_disable("x11")
        args += self.with_or_without("fftw")

        # possible future variants
        args.extend(
            [
                "--disable-asyncns",
                "--disable-avahi",
                "--disable-bluez5",
                "--disable-gcov",
                "--disable-gsettings",
                "--disable-gtk3",
                "--disable-hal-compat",
                "--disable-jack",
                "--disable-lirc",
                "--disable-orc",
                "--disable-tcpwrap",
            ]
        )

        return args

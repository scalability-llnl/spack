# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsamplerate(AutotoolsPackage):
    """libsamplerate (also known as Secret Rabbit Code) is a library for
    performing sample rate conversion of audio data."""

    homepage = "http://libsndfile.github.io/libsamplerate/"
    url = "https://github.com/libsndfile/libsamplerate/releases/download/0.2.2/libsamplerate-0.2.2.tar.xz"

    license("BSD-2-Clause")

    version("0.2.2", sha256="3258da280511d24b49d6b08615bbe824d0cacc9842b0e4caf11c52cf2b043893")
    version("0.1.9", sha256="0a7eb168e2f21353fb6d84da152e4512126f7dc48ccb0be80578c565413444c1")
    version("0.1.8", sha256="93b54bdf46d5e6d2354b7034395fe329c222a966790de34520702bb9642f1c06")

    depends_on("c", type="build")

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def url_for_version(self, version):
        if self.spec.satisfies("@2.2:"):
            return f"https://github.com/libsndfile/libsamplerate/releases/download/{version}/libsamplerate-{version}.tar.xz"
        elif self.spec.satisfies("@2:2.1"):
            return f"https://github.com/libsndfile/libsamplerate/releases/download/{version}/libsamplerate-{version}.tar.bz2"
        else:
            return f"http://www.mega-nerd.com/libsamplerate/libsamplerate-{version}.tar.gz"

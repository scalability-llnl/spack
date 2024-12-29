# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsndfile(AutotoolsPackage):
    """Libsndfile is a C library for reading and writing files containing
    sampled sound (such as MS Windows WAV and the Apple/SGI AIFF format)
    through one standard library interface. It is released in source code
    format under the Gnu Lesser General Public License."""

    homepage = "https://github.com/libsndfile/libsndfile"
    url = (
        "https://github.com/libsndfile/libsndfile/releases/download/1.2.2/libsndfile-1.2.2.tar.xz"
    )

    license("LGPL-2.1-or-later")

    version("1.2.2", sha256="3799ca9924d3125038880367bf1468e53a1b7e3686a934f098b7e1d286cdb80e")
    # https://nvd.nist.gov/vuln/detail/CVE-2022-33064
    version(
        "1.0.28",
        sha256="1ff33929f042fa333aed1e8923aa628c3ee9e1eb85512686c55092d1e5a9dfa9",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("alsa", default=False, description="Use alsa in example programs")
    variant(
        "external-libs", default=False, description="Build with support for FLAC, Ogg and Vorbis"
    )
    variant("sqlite", default=False, description="Build with sqlite support")

    depends_on("pkgconfig", type="build")
    depends_on("alsa-lib", when="+alsa")
    depends_on("flac@1.3.1:", when="+external-libs")
    depends_on("libogg@1.1.3:", when="+external-libs")
    depends_on("libogg@1.3.0:", when="@1.0.31: +external-libs")
    depends_on("libvorbis@1.2.3:", when="+external-libs")
    depends_on("sqlite@3.2:", when="+sqlite")

    def url_for_version(self, version):
        if self.spec.satisfies("@1.1:"):
            return f"https://github.com/libsndfile/libsndfile/releases/download/{version}/libsndfile-{version}.tar.xz"
        elif self.spec.satisfies("@1.0.29:"):
            return f"https://github.com/libsndfile/libsndfile/releases/download/v{version}/libsndfile-{version}.tar.bz2"
        else:
            return f"http://www.mega-nerd.com/libsndfile/files/libsndfile-{version}.tar.gz"

    def configure_args(self):
        args = []

        args += self.enable_or_disable("alsa")
        args += self.enable_or_disable("external-libs")
        args += self.enable_or_disable("sqlite")

        return args

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nghttp2(AutotoolsPackage):
    """nghttp2 is an implementation of HTTP/2 and its header compression
    algorithm HPACK in C."""

    homepage = "https://nghttp2.org/"
    url = "https://github.com/nghttp2/nghttp2/releases/download/v1.26.0/nghttp2-1.26.0.tar.gz"

    license("MIT")

    version("1.63.0", sha256="9318a2cc00238f5dd6546212109fb833f977661321a2087f03034e25444d3dbb")
    version("1.62.1", sha256="d0b0b9d00500ee4aa3bfcac00145d3b1ef372fd301c35bff96cf019c739db1b4")
    version("1.62.0", sha256="482e41a46381d10adbdfdd44c1942ed5fd1a419e0ab6f4a5ff5b61468fe6f00d")
    version("1.61.0", sha256="aa7594c846e56a22fbf3d6e260e472268808d3b49d5e0ed339f589e9cc9d484c")
    version("1.59.0", sha256="90fd27685120404544e96a60ed40398a3457102840c38e7215dc6dec8684470f")
    version("1.57.0", sha256="1e3258453784d3b7e6cc48d0be087b168f8360b5d588c66bfeda05d07ad39ffd")
    version("1.52.0", sha256="9877caa62bd72dde1331da38ce039dadb049817a01c3bdee809da15b754771b8")
    version("1.51.0", sha256="2a0bef286f65b35c24250432e7ec042441a8157a5b93519412d9055169d9ce54")
    version("1.50.0", sha256="d162468980dba58e54e31aa2cbaf96fd2f0890e6dd141af100f6bd1b30aa73c6")
    version("1.48.0", sha256="66d4036f9197bbe3caba9c2626c4565b92662b3375583be28ef136d62b092998")
    version("1.47.0", sha256="62f50f0e9fc479e48b34e1526df8dd2e94136de4c426b7680048181606832b7c")
    version("1.44.0", sha256="3e4824d02ae27eca931e0bb9788df00a26e5fd8eb672cf52cbb89c1463ba16e9")
    version("1.26.0", sha256="daf7c0ca363efa25b2cbb1e4bd925ac4287b664c3d1465f6a390359daa3f0cf1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("diffutils", type="build")

    def configure_args(self):
        return [
            "--enable-lib-only",
            "--with-libxml2=no",
            "--with-jansson=no",
            "--with-zlib=no",
            "--with-libevent-openssl=no",
            "--with-libcares=no",
            "--with-openssl=no",
            "--with-libev=no",
            "--with-cunit=no",
            "--with-jemalloc=no",
            "--with-systemd=no",
            "--with-mruby=no",
            "--with-neverbleed=no",
            "--with-boost=no",
            "--with-wolfssl=no",
        ]

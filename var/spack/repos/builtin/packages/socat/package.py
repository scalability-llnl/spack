# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Socat(AutotoolsPackage):
    """socat is a relay for bidirectional data transfer between two independent
    data channels. Each of these data channels may be a file, pipe, device
    (serial line etc. or a pseudo terminal), a socket (UNIX, IP4, IP6 - raw,
    UDP, TCP), an SSL socket, proxy CONNECT connection, a file descriptor
    (stdin etc.), the GNU line editor (readline), a program, or a combination
    of two of these. These modes include generation of "listening" sockets,
    named pipes, and pseudo terminals."""

    homepage = "http://www.dest-unreach.org/socat/"
    url = "http://www.dest-unreach.org/socat/download/socat-1.7.4.4.tar.bz2"

    maintainers("michaelkuhn")

    license("GPL-2.0-only WITH OpenSSL-Exception")

    version("1.7.4.4", sha256="fbd42bd2f0e54a3af6d01bdf15385384ab82dbc0e4f1a5e153b3e0be1b6380ac")

    depends_on("c", type="build")  # generated

    depends_on("openssl")
    depends_on("readline")
    depends_on("ncurses")

    def configure_args(self):
        args = ["--disable-libwrap"]
        return args

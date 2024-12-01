# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Httping(AutotoolsPackage):
    """Httping is like 'ping' but for http-requests. Give it an url,
    and it'll show you how long it takes to connect, send a request
    and retrivee the reply(only the headers), Be aware that the
    transmission across the network also takes time! So it measures
    the latency. of the webserver + network. It supports, of course,
    IPv6. httping was analyzed by Coverity Scan for software defects."""

    homepage = "https://www.vanheusden.com/httping/"
    url = "https://github.com/flok99/httping/archive/2.5.tar.gz"

    license("GPL-2.0-or-later")

    version("2.5", sha256="2ad423097fa7a0d2d20a387050e34374326a703dddce897e152a8341e47ea500")
    version("2.3.4", sha256="45ed71a72fd8c9c3975e49706c739395f75e3977b91f96e7e25652addfa0f242")
    version("2.3.3", sha256="b76ec14cb4f6cd29b60a974254f4be37ed721c1660ecde9f6aac516ba521ab86")
    version("2.3.1", sha256="90e86ca98f6c6bd33bd23a0eeda6f994dd8d147971d402da2733746c9b6ee61c")
    version("2.3", sha256="5d87e59e5d9e216346769471b581f289eac5e49cfc969407c199761367553ca8")

    def install(self, spec, prefix):
        make("install", "PREFIX={0}".format(prefix))

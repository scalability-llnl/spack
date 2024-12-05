# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Audacious(AutotoolsPackage):
    """A lightweight and versatile audio player."""

    homepage = "https://audacious-media-player.org/"
    url = "https://github.com/audacious-media-player/audacious/archive/audacious-4.0.2.tar.gz"

    license("BSD-2-Clause AND BSD-3-Clause", checked_by="tgamblin")

    version("4.0.2", sha256="92f30a78353c50f99b536061b9d94b6b9128760d546fddbf863e3591c4ac5a8d")
    version("4.0.1", sha256="203195cf0d3c2e40d23c9895269ca0ace639c4a2b4dceb624169d75337059985")
    version("4.0", sha256="cdfffd0eb966856980328ebb0fff9cbce57f99db9bda15e7e839d26c89e953e6")
    version("3.10.1", sha256="c478939b4bcf6704c26eee87d48cab26547e92a83741f437711178c433373fa1")
    version("3.10", sha256="82710d6ac90931c2cc4a0f0fcb6380ac21ed42a7a50856d16a67d3179a96e9ae")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("gettext")
    depends_on("iconv", type="link")
    depends_on("glib")
    depends_on("qt")

    def patch(self):
        search_path_args = " ".join(self.autoreconf_search_path_args)
        search_path_str = f"-I m4 {search_path_args}"
        filter_file("-I m4", search_path_str, "autogen.sh")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

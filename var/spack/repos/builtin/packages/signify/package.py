# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Signify(MakefilePackage):
    """OpenBSD tool to signs and verify signatures on files."""

    homepage = "https://github.com/aperezdc/signify"
    url = "https://github.com/aperezdc/signify/archive/v23.tar.gz"

    license("ISC")

    version("32", sha256="48cfd7bfe55be01909b37e78045f240b950ea51c954bab205bcdcddc0492dca4")
    version("31", sha256="8111af7424f4cc69dab5cd43a14ccd607ca2d171ac77dd3ae288264a53254e5f")
    version("23", sha256="1c690bf0e4283e0764a4a9dd784cb3debf4bb456b975b275dd1aaac7d5afe030")

    depends_on("c", type="build")  # generated

    depends_on("libbsd@0.8:")

    def setup_build_environment(self, env):
        env.set("PREFIX", self.prefix)

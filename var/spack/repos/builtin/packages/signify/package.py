# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Signify(MakefilePackage):
    """OpenBSD tool to signs and verify signatures on files."""

    homepage = "https://github.com/aperezdc/signify"
    url      = "https://github.com/aperezdc/signify/archive/v23.tar.gz"

    version('23', sha256='1c690bf0e4283e0764a4a9dd784cb3debf4bb456b975b275dd1aaac7d5afe030')

    depends_on('libbsd@0.8:')

    def setup_build_environment(self, env):
        env.set('PREFIX', self.prefix)

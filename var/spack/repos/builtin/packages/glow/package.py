# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glow(GoPackage):
    """Render markdown on the CLI, with pizzazz!"""

    homepage = "https://github.com/charmbracelet/glow"
    url      = "https://github.com/charmbracelet/glow/archive/v0.1.6.tar.gz"

    version('0.1.6', sha256='a0848b1f4865251e445b6d88e98cbc44a4dfa835fc0a705fb79c1ed372bef2bc')

    depends_on('go@1.13:', type='build')  # go.mod value overrides default

    import_resources('resources-0.1.6.json')

    executables = ['glow']

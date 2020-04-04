# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hugo(GoPackage):
    """The world's fastest framework for building websites."""

    homepage = "https://gohugo.io"
    url      = "https://github.com/gohugoio/hugo/archive/v0.53.tar.gz"

    version('0.53', sha256='48e65a33d3b10527101d13c354538379d9df698e5c38f60f4660386f4232e65c')

    variant('extended', default='False', description='Extended Sass/SCSS support')

    # hugo has used modules since its v0.48, so we do too.
    import_resources("hugo-resources-0.53.json")

    def build_args(self):
        if self.spec.satisfies('+extended'):
            return ['-tags', 'extended']
        return []

    executables = ['hugo']

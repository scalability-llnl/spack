# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

from llnl.util.lang import match_predicate


class Umoci(MakefilePackage):
    """umoci modifies Open Container images, intending to be a
    complete manipulation tool for OCI images."""

    homepage = "https://umo.ci/"
    url      = "https://github.com/openSUSE/umoci/archive/v0.4.4.tar.gz"

    version('0.4.4', sha256='bc5c53812e0076d026aa275b197b878857cf7ba7a4f048fd13433de6107b9aed')
    version('0.4.3', sha256='b7d537fec84d4327b1bbfe27118f69df5591143a74a7a1b66cc9904d85c30226')

    depends_on('go@1.11:')
    depends_on('go-md2man', type='build')

    # touch up project's Makefile so that it runs go in module mode and
    # uses the project's vendored dependencies
    # this works for @0.4.2:
    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('export GO111MODULE=off',
                        'export GO111MODULE=on', string=True)
        makefile.filter('PROJECT := github.com/openSUSE/umoci',
                        'PROJECT := .', string=True)
        makefile.filter('BUILD_FLAGS ?=',
                        'BUILD_FLAGS ?= -mod=vendor', string=True)

    def build(self, spec, prefix):
        make()
        if spec.satisfies("@0.4.3"):
            make('doc')

    def install(self, spec, prefix):
        if spec.satisfies("@0.4.4"):
            make('PREFIX=', 'DESTDIR={0}'.format(prefix), 'install')
        if spec.satisfies("@0.4.3"):
            mkdirp(prefix.bin)
            install('umoci', prefix.bin)
            matcher = match_predicate(r'.md$')
            ignore = lambda p: matcher(p)
            mkdirp(prefix.share.man.man1)
            install_tree('doc/man', prefix.share.man.man1, ignore=ignore)

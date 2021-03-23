# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from spack.pkg.builtin.boost import Boost


class SourceHighlight(AutotoolsPackage, GNUMirrorPackage):
    """This program, given a source file, produces a document with syntax
    highlighting. It also provides a C++ highlight library
    (since version 3.0). """

    homepage = "https://www.gnu.org/software/src-highlite/"
    gnu_mirror_path = "src-highlite/source-highlight-3.1.8.tar.gz"

    version('3.1.9', sha256='3a7fd28378cb5416f8de2c9e77196ec915145d44e30ff4e0ee8beb3fe6211c91')
    version('3.1.8', sha256='01336a7ea1d1ccc374201f7b81ffa94d0aecb33afc7d6903ebf9fbf33a55ada3')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    def configure_args(self):
        args = ["--with-boost={0}".format(self.spec['boost'].prefix)]
        return args

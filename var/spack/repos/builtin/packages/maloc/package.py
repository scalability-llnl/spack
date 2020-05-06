# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install maloc
#
# You can edit this file again by typing:
#
#     spack edit maloc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Maloc(AutotoolsPackage):
    """MALOC (Minimal Abstraction Layer for Object-oriented C)
    is a small, portable, abstract C environment library for
    object-oriented C programming. MALOC is used as the
    foundation layer for a number of scientific applications,
    including MC, SG, and APBS. MALOC can be used as a small
    stand-alone abstraction environment for writing portable C
    programs which need access to resources which are typically
    architecture-dependent, such as INET sockets, timing
    routines, and so on. MALOC provides abstract datatypes,
    memory management routines, timing routines, machine
    epsilon, access to UNIX and INET sockets, MPI, and so on.
    All things that can vary from one architecture to another
    are abstracted out of an application code and placed in
    MALOC. To port the application code to a new architecture,
    only the small MALOC library needs to be ported (usually
    just "./configure ; make"). MALOC takes the pain of varying
    UNIX (and Win32) platforms with differing library and
    header layous completely out of the software development
    picture."""


    homepage = "http://fetk.org/codes/maloc/"
    url      = "http://www.fetk.org/codes/download/maloc-1.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('1.5', sha256='58e1197fcd4c74d3cbb1d39d712eb0a3c5886a1e6629f22c5c78ce2bac983fc0')
    version('1.4', sha256='cba0c6730f148bf7ddb77dac07e497655642f43b632256fcebf3192b45af1833')
    version('1.3', sha256='337788ac8f263487aba5b3aa5ef7f33eaac1d3951ad49349078d5ed77482ad2e')
    version('1.2', sha256='e6033195a054bad7527d360e52349a4d1eb876c681a58fa373f42fd1ab26962c')
    version('1.1', sha256='b5dd7923e84f13e7ed43304ed1062de24171c5a7a042a12b0d1e501d6eaedf58')
    version('1.0', sha256='23f3ea3215067fd8f1ba4c407375f387b5f1d11258f29508295e651828d32cb7')

    variant('doc', default=False, description='Build documentation.')

    depends_on('graphviz', type='build', when='+doc')
    depends_on('doxygen', type='build', when='+doc')

    def configure_args(self):
        spec = self.spec
        args = []

        if '~doc' in spec:
            args.append('--with-doxygen=no')
            args.append('--with-dot=no')

        return args

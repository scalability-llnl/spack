# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Byacc(AutotoolsPackage):
    """Berkeley Yacc is an LALR(1) parser generator.  Berkeley Yacc has
    been made as compatible as possible with AT&T Yacc.  Berkeley Yacc
    can accept any input specification that conforms to the AT&T Yacc
    documentation. Specifications that take advantage of undocumented
    features of AT&T Yacc will probably be rejected."""

    homepage = "https://github.com/grandseiken/byacc"
    git      = "https://github.com/grandseiken/byacc.git"

    version('master', branch='master')

    provides('yacc')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

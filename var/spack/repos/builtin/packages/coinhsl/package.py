##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os


class Coinhsl(AutotoolsPackage):
    """CoinHSL is a collection of linear algebra libraries (KB22, MA27,
    MA28, MA54, MA57, MA64, MA77, MA86, MA97, MC19, MC34, MC64, MC68,
    MC69, MC78, MC80, OF01, ZB01, ZB11) bundled for use with IPOPT and
    other applications that use these HSL routines.

    Note: CoinHSL is licensed software. You will need to request a
    license from Research Councils UK and download a .tar.gz archive
    of CoinHSL yourself. Spack will search your current directory for
    the download file. Alternatively, add this file to a mirror so
    that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    # NOTE(oxberry1@llnl.gov): an HTTPS version of the URL below does not
    # exist
    homepage = "http://www.hsl.rl.ac.uk/ipopt/"
    url = "file://{0}/coinhsl-archive-2014.01.17.tar.gz".format(os.getcwd())

    # CoinHSL has a few versions that vary with respect to stability/features
    # and licensing terms.

    # Version 2015.06.23 is a full-featured "release candidate"
    # version available via an "academic license" that can be used for
    # personal teaching and research purposes only. For a full list of
    # conditions, see http://www.hsl.rl.ac.uk/academic.html.
    version('2015.06.23', sha256='3e955a2072f669b8f357ae746531b37aea921552e415dc219a5dd13577575fb3')

    # Version 2014.01.17 is a full-featured "stable" version available
    # via an "academic license" that can be used for personal teaching
    # and research purposes only.
    version('2014.01.17', sha256='ed49fea62692c5d2f928d4007988930da9ff9a2e944e4c559d028671d122437b')

    # Version 2014.01.10 only has MA27, MA28, and MC19, and is
    # available as a "personal license" that is free to all, and
    # permits commercial use, but *not redistribution* (emphasis from
    # original source).
    version('2014.01.10', sha256='7c2be60a3913b406904c66ee83acdbd0709f229b652c4e39ee5d0876f6b2e907',
            preferred=True)

    # CoinHSL fails to build in parallel
    parallel = False

    variant('blas', default=False, description='Link to external BLAS library')

    depends_on('blas', when='+blas')

    def configure_args(self):
        spec = self.spec
        args = []

        if spec.satisfies('+blas'):
            args.append('--with-blas={0}'.format(spec['blas'].libs.ld_flags))

        return args

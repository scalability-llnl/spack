# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    manual_download = True

    # CoinHSL has a few versions that vary with respect to stability/features
    # and licensing terms.

    # Version 2019.05.21 is a full-featured "release candidate"
    # version available via an "academic license" that can be used for
    # personal teaching and research purposes only. For a full list of
    # conditions, see http://www.hsl.rl.ac.uk/academic.html.
    version('2019.05.21', sha256='95ce1160f0b013151a3e25d40337775c760a8f3a79d801a1d190598bf4e4c0c3')

    # Version 2015.06.23 is a full-featured "stable"
    # version available via an "academic license" that can be used for
    # personal teaching and research purposes only. For a full list of
    # conditions, see http://www.hsl.rl.ac.uk/academic.html.
    version('2015.06.23', sha256='3e955a2072f669b8f357ae746531b37aea921552e415dc219a5dd13577575fb3',
            preferred=True)

    # Version 2014.01.17 is a full-featured "stable" version available
    # via an "academic license" that can be used for personal teaching
    # and research purposes only.
    version('2014.01.17', sha256='ed49fea62692c5d2f928d4007988930da9ff9a2e944e4c559d028671d122437b')

    # Version 2014.01.10 only has MA27, MA28, and MC19, and is
    # available as a "personal license" that is free to all, and
    # permits commercial use, but *not redistribution* (emphasis from
    # original source).
    version('2014.01.10', sha256='7c2be60a3913b406904c66ee83acdbd0709f229b652c4e39ee5d0876f6b2e907')

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

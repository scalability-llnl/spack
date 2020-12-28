# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Star(Package):
    """STAR is an ultrafast universal RNA-seq aligner."""

    homepage = "https://github.com/alexdobin/STAR"
    url      = "https://github.com/alexdobin/STAR/archive/2.7.6a.tar.gz"

    version('2.7.6a', sha256='9320797c604673debea0fe8f2e3762db364915cc59755de1a0d87c8018f97d51')
    version('2.7.0e', sha256='2fc9d9103bd02811904d41e3a3d50e47c7de17cb55c3b4880ea5f39300a9ba0d')
    version('2.7.0d', sha256='7a757478868dc73fe7619bf6ea302dd642bd30e1c8c1fb4acdbe7fa151cf9fd1')
    version('2.6.1b', sha256='1bba5b26c1e6e9a7aca8473a99dbf37bad1dbdd0a589402448e278553bb6b3da')
    version('2.6.1a', sha256='dc87357211432c05123ce49966aae712dec590cbe27c1fd0193c3aeb8d4abe4b')
    version('2.6.0c', sha256='bebba6cc72da302429c44c20f3b07bdde6b0ddf33e538a99e297f1d342070387')
    version('2.6.0b', sha256='1ebbecbb698a3de95990b35fe386189a2c00b07cd9d2d4e017ab8234e7dc042e')
    version('2.6.0a', sha256='a6b0dd1918e1961eebec71e6c7c3c8e632f66d10e0620aa09c0710e2ab279179')
    version('2.5.4b', sha256='bfa6ccd3b7b3878155a077a9c15eec5490dffad8e077ac93abe6f9bfa75bb2b4')
    version('2.5.4a', sha256='17b02703cdd580c9fd426a14f20712ea252d32a4ded804eef759029b600e3afb')
    version('2.5.3a', sha256='2a258e77cda103aa293e528f8597f25dc760cba188d0a7bc7c9452f4698e7c04')
    version('2.5.2b', sha256='f88b992740807ab10f2ac3b83781bf56951617f210001fab523f6480d0b546d9')
    version('2.5.2a', sha256='2a372d9bcab1dac8d35cbbed3f0ab58291e4fbe99d6c1842b094ba7449d55476')
    version('2.4.2a', sha256='ac166d190c0fd34bf3418a5640050b0e7734d279813e02daa013d0924fb579b0', url='https://github.com/alexdobin/STAR/archive/STAR_2.4.2a.tar.gz')

    depends_on('zlib')

    def install(self, spec, prefix):
        with working_dir('source'):
            make('STAR', 'STARlong')
            mkdirp(prefix.bin)
            install('STAR', prefix.bin)
            install('STARlong', prefix.bin)

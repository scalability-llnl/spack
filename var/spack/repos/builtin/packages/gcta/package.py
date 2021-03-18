# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gcta(Package):

    """GCTA (Genome-wide Complex Trait Analysis) was originally designed to
    estimate the proportion of phenotypic variance explained by all genome-wide
    SNPs for complex traits (the GREML method), and has subsequently extended
    for many other analyses to better understand the genetic architecture of
    complex traits. GCTA currently supports the following analyses."""

    homepage = "http://cnsgenomics.com/software/gcta/#Overview"
    url      = "https://cnsgenomics.com/software/gcta/bin/gcta_1.93.1beta.zip"

    version('1.93.1beta_mac', '86fb7f1885beaa3e35d39a89c9ac9522d5b337bffcfc2194fc2f886d13cda823')
    version('1.93.1beta', 'e6439fc0173642d917a039dbdc6a8cb5b309f76d4f56762212b1a760a2c8a678', preferred=True)
    version('1.91.2beta_mac', 'ce0882ad35dd9474ffe40911da369274700af1ecb9916c0a355b7bad14850234', deprecated=True)
    version('1.91.2beta', '192efb767be1c7ca9c2dac5d2c2317a97c7a9db1f801168d19ad2a51b98d9b10', deprecated=True)

    conflicts('@1.93.1beta', when='platform=darwin')
    conflicts('@1.93.1beta_mac', when='platform=linux')
    conflicts('@1.91.2beta', when='platform=darwin')
    conflicts('@1.91.2beta_mac', when='platform=linux')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('gcta64', join_path(prefix.bin, 'gcta64'))
        set_executable(join_path(prefix.bin, 'gcta64'))

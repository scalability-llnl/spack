# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Plink(Package):
    """PLINK is a free, open-source whole genome association analysis toolset,
       designed to perform a range of basic, large-scale analyses in a
       computationally efficient manner."""

    homepage = "https://www.cog-genomics.org/plink/1.9/"

    version('1.9-beta6.10', sha256='f8438656996c55a5edd95c223cce96277de6efaab1b9b1d457bfee0c272058d8',
            url='http://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20190617.zip')
    version('1.9-beta5', sha256='e00ef16ac5abeb6b4c4d77846bd655fafc62669fbebf8cd2e941f07b3111907e',
            url='https://github.com/chrchang/plink-ng/archive/b15c19f.tar.gz')
    version('1.07', sha256='70c52ee47eed854293832639dbabb41c7c036db3a4881c136e6a71ecff4ac7f4',
            url='http://zzz.bwh.harvard.edu/plink/dist/plink-1.07-x86_64.zip',
            preferred=True)

    depends_on('atlas', when='@1.9-beta5')
    depends_on('netlib-lapack', when='@1.9-beta5')
    depends_on('atlas', when='@1.9-beta6.10')
    depends_on('netlib-lapack', when='@1.9-beta6.10')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if spec.version == Version('1.07'):
            install('plink', prefix.bin)
            install('gPLINK.jar', prefix.bin)
        if spec.version == Version('1.9-beta5'):
            with working_dir('1.9'):
                first_compile = Executable('./plink_first_compile')
                first_compile()
                install('plink', prefix.bin)
        if spec.version == Version('1.9-beta6.10'):
            install('plink', prefix.bin)

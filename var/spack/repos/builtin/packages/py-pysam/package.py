# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysam(PythonPackage):
    """A python module for reading, manipulating and writing genomic data
       sets."""

    homepage = "https://pypi.python.org/pypi/pysam"
    url      = "https://github.com/pysam-developers/pysam/archive/v0.14.1.tar.gz"

    version('0.15.2', sha256='8cb3dd70f0d825086ac059ec2445ebd2ec5f14af73e7f1f4bd358966aaee5ed3')
    version('0.15.1', sha256='12221285af17e32b8f3fed033f90c6177a798afe41420eb5c3352d4e18ee12ed')
    version('0.14.1', sha256='d2bb40cd083c1357768e4683377f03471d160cfe8421136630bfa47f5adb3219')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.21:', type='build')
    depends_on('curl')
    depends_on('bcftools')
    depends_on('htslib')
    depends_on('samtools')

    depends_on('htslib@:1.6', when='@:0.13')

    def setup_build_environment(self, env):
        env.set('LDFLAGS', self.spec['curl'].libs.search_flags)

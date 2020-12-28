# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glog(Package):
    """C++ implementation of the Google logging module."""

    homepage = "https://github.com/google/glog"
    url      = "https://github.com/google/glog/archive/v0.3.5.tar.gz"

    version('0.4.0', sha256='f28359aeba12f30d73d9e4711ef356dc842886968112162bc73002645139c39c')
    version('0.3.5', sha256='7580e408a2c0b5a89ca214739978ce6ff480b5e7d8d7698a2aa92fadc484d1e0')
    version('0.3.4', sha256='ce99d58dce74458f7656a68935d7a0c048fa7b4626566a71b7f4e545920ceb10')
    version('0.3.3', sha256='544e178644bd9b454768c2c91716c3b8365cc5d47adfbdbaecd8cf3fa17adfcb')

    depends_on('gflags')
    depends_on('cmake', when="@0.3.5:", type='build')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make('install')

    @when('@0.3.5:')
    def install(self, spec, prefix):
        cmake_args = ['-DBUILD_SHARED_LIBS=TRUE']
        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)
            make()
            make('install')

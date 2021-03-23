# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost
import os.path
import glob


class Express(CMakePackage):
    """eXpress is a streaming tool for quantifying the abundances of a set of
       target sequences from sampled subsequences."""

    homepage = "http://bio.math.berkeley.edu/eXpress/"
    url      = "https://github.com/adarob/eXpress/archive/1.5.2.zip"

    # 1.5.1 used to be known as 2015-11-29 (same commit), but they've
    # added tags, so lets use 'em
    version('1.5.2', sha256='25a63cca3dac6bd0daf04d2f0b2275e47d2190c90522bd231b1d7a875a59a52e')
    version('1.5.1', sha256='fa3522de9cc25f1ede22fa196928912a6da2a2038681911115ec3e4da3d61293')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('bamtools')
    depends_on('zlib')

    # patch from the debian package repo:
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=811859
    patch('gcc-6.patch', when='%gcc@6.0.0:')
    patch('gcc-6.patch', when='%fj')

    def patch(self):
        with working_dir('src'):
            files = glob.iglob('*.*')
            for file in files:
                if os.path.isfile(file):
                    edit = FileFilter(file)
                    edit.filter('#include <api', '#include <%s' % self.spec[
                                'bamtools'].prefix.include.bamtools.api)
            edit = FileFilter('CMakeLists.txt')
            edit.filter(r'\${CMAKE_CURRENT_SOURCE_DIR}/../bamtools/lib/'
                        'libbamtools.a', '%s' % self.spec['bamtools'].libs)

    def setup_build_environment(self, env):
        env.prepend_path('CPATH',
                         self.spec['bamtools'].prefix.include.bamtools)

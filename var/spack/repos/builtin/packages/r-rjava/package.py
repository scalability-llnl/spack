# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRjava(RPackage):
    """Low-Level R to Java Interface

    Low-level interface to Java VM very much like .C/.Call and friends.
    Allows creation of objects, calling methods and accessing fields."""

    homepage = "http://www.rforge.net/rJava/"
    url      = "https://cloud.r-project.org/src/contrib/rJava_0.9-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rJava"

    version('0.9-13', sha256='5b1688f5044476b34f71d868b222ac5fce3a088f0c2b9e4591c1e48f3d8c75f4')
    version('0.9-11', sha256='c28ae131456a98f4d3498aa8f6eac9d4df48727008dacff1aa561fc883972c69')
    version('0.9-8', sha256='dada5e031414da54eb80b9024d51866c20b92d41d68da65789fe0130bc54bd8a')

    depends_on('r@2.5:', type=('build', 'run'))
    depends_on('java@2:')
    depends_on('gmake', type='build')

    # these are not listed as dependencies but are needed
    depends_on('bzip2')
    depends_on('icu4c')
    depends_on('libiconv')
    depends_on('pcre2')
    depends_on('xz')

    def setup_build_environment(self, env):
        spec = self.spec
        env.append_flags('JAVAH', '{0}/javah'.format(
            join_path(spec['java'].prefix.bin)))

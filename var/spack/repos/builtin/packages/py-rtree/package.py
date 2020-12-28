# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRtree(PythonPackage):
    """Python interface to the RTREE.4 Library."""
    homepage = "http://toblerity.org/rtree/"
    url      = "https://pypi.io/packages/source/R/Rtree/Rtree-0.8.3.tar.gz"

    version('0.8.3', sha256='6cb9cf3000963ea6a3db777a597baee2bc55c4fc891e4f1967f262cc96148649')

    depends_on('py-setuptools', type='build')
    depends_on('libspatialindex')

    def setup_build_environment(self, env):
        lib = self.spec['libspatialindex'].prefix.lib
        env.set('SPATIALINDEX_LIBRARY',
                join_path(lib, 'libspatialindex.%s'   % dso_suffix))
        env.set('SPATIALINDEX_C_LIBRARY',
                join_path(lib, 'libspatialindex_c.%s' % dso_suffix))

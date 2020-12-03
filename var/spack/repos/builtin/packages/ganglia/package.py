# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

from spack.util.provides import setup_libtirpc_build_environment


class Ganglia(AutotoolsPackage):
    """Ganglia is a scalable distributed monitoring system for high-performance
    computing systems such as clusters and Grids. It is based on a hierarchical
    design targeted at federations of clusters. Supports clusters up to 2000
    nodes in size."""

    homepage = "http://ganglia.sourceforge.net/"
    url      = "http://jaist.dl.sourceforge.net/project/ganglia/ganglia%20monitoring%20core/3.7.2/ganglia-3.7.2.tar.gz"
    list_url = "http://jaist.dl.sourceforge.net/project/ganglia/ganglia%20monitoring%20core"
    list_depth = 1

    version('3.7.2', sha256='042dbcaf580a661b55ae4d9f9b3566230b2232169a0898e91a797a4c61888409')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('apr')
    depends_on('libconfuse')
    depends_on('python@:2.7.999')
    depends_on('pcre')
    depends_on('libtirpc')
    depends_on('expat')

    def setup_build_environment(self, env):
        setup_libtirpc_build_environment(self.spec, env)

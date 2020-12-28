# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ambari(PythonPackage):
    """Apache Ambari is a tool for provisioning, managing, and monitoring
    Apache Hadoop clusters. Ambari consists of a set of RESTful APIs and
    a browser-based management interface."""

    homepage = "https://cwiki.apache.org/confluence/display/AMBARI/Ambari"
    url      = "https://github.com/apache/ambari/archive/release-2.7.5.tar.gz"

    version('2.7.5', sha256='f8c8687b7a61b633b92f83b1c104fd75b1e13836cd8a0e0df6db7b483b23a354')
    version('2.7.4', sha256='d6796c7ea913d39c93dad52b4cb74ef411a7dce4ebf68f11b12718117f2c01a4')
    version('2.7.3', sha256='30fe72e60fa6b62fe032bd193ebd0cef20b65c54b57cad92f6f44daabd3771cf')
    version('2.7.1', sha256='ea4eb28f377ce9d0b9b7648f2020dda4be974c6d9a22ebaafbf1bc97890e4e42')

    depends_on('python@:2.7.999', type=('build', 'run'))
    depends_on('py-setuptools@:44.99.99', type='build')
    depends_on('py-mock', type='test')
    depends_on('py-coilmq', type=('build', 'run'))

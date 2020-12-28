# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibcapNg(AutotoolsPackage):
    """Libcap-ng is a library that makes using posix capabilities easier"""

    homepage = "https://github.com/stevegrubb/libcap-ng/"
    url      = "https://github.com/stevegrubb/libcap-ng/archive/v0.8.tar.gz"

    version('0.8',    sha256='836ea8188ae7c658cdf003e62a241509dd542f3dec5bc40c603f53a5aadaa93f')
    version('0.7.11', sha256='78f32ff282b49b7b91c56d317fb6669df26da332c6fc9462870cec2573352222')
    version('0.7.10', sha256='c3c156a215e5be5430b2f3b8717bbd1afdabe458b6068a8d163e71cefe98fc32')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('attr',     type='build')
    depends_on('python',   type=('build', 'run'))

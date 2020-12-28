# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastjson(MavenPackage):
    """Fastjson is a Java library that can be used to convert Java Objects
    into their JSON representation. It can also be used to convert a JSON
    string to an equivalent Java object. """

    homepage = "https://github.com/alibaba/fastjson/wiki"
    url      = "https://github.com/alibaba/fastjson/archive/1.2.68.tar.gz"

    version('1.2.68', sha256='0b3f5308830e5e5abacf9dc8e4115c20153c1cdabec228c3eca48a48c9d5f4d7')

    depends_on('java@8', type=('build', 'run'))

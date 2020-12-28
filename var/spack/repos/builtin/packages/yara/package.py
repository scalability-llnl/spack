# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yara(AutotoolsPackage):
    """YARA is a tool aimed at (but not limited to) helping malware researchers
    to identify and classify malware samples"""

    homepage = "http://virustotal.github.io/yara/"
    url      = "https://github.com/VirusTotal/yara/archive/v3.9.0.tar.gz"

    version('3.9.0', sha256='ebe7fab0abadb90449a62afbd24e196e18b177efe71ffd8bf22df95c5386f64d')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

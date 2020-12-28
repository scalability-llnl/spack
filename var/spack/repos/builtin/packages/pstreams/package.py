# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pstreams(Package):
    """C++ wrapper for the POSIX.2 functions popen(3) and pclose(3)"""

    homepage = "http://pstreams.sourceforge.net/"
    url      = "https://sourceforge.net/projects/pstreams/files/pstreams/Release%201.0/pstreams-1.0.1.tar.gz"

    version('1.0.1', sha256='a5f1f2e014392cd0e2cdb508a429e11afe64140db05b7f0a83d7534faa1a9226')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install('pstream.h', prefix.include)

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class MadNumdiff(CMakePackage):
    """compare unformatted text files with numerical content"""

    homepage = "https://github.com/quinoacomputing/ndiff"
    url      = "https://github.com/quinoacomputing/ndiff/tarball/20150724"
    git      = "https://github.com/quinoacomputing/ndiff.git"

    version('develop', branch='master')
    version('20150724', sha256='33130b48416f8dcb6402acbcb8906cdec35b7242fe2f3ad49b7d7c063d75377b')

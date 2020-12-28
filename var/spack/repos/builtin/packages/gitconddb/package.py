# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gitconddb(CMakePackage):
    """Conditions Database library using a Git repository as the
    storage backend"""

    homepage = "https://gitlab.cern.ch/lhcb/GitCondDB"
    url      = "https://gitlab.cern.ch/lhcb/GitCondDB/-/archive/0.1.1/GitCondDB-0.1.1.tar.gz"
    git      = "https://gitlab.cern.ch/lhcb/GitCondDB.git"

    maintainers = ['drbenmorgan']

    version('master', branch='master')
    version('0.1.1', sha256='024a6867722a3a622ed4327ea7d15641dd48e4e8411bdcc21915e406b3c479a2')

    # Add the cxxstd variant for forward compatibility, though we require 17
    _cxxstd_values = ('17',)
    variant('cxxstd',
            default='17',
            values=_cxxstd_values,
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake@3.10:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('nlohmann-json@3.2.0:', type='build')
    depends_on('googletest@1.8.1:', type='build')

    for s in _cxxstd_values:
        depends_on('fmt@5.2.0: cxxstd=' + s, when='cxxstd=' + s)
        # Maybe also a boost dependency for macOS older than catalina

    depends_on('libgit2')

    # Known conflicts on C++17 compatibility (aggressive for now)
    conflicts('%gcc@:7.9.999', msg="GitCondDB requires GCC 8 or newer for C++17 support")
    conflicts('%apple-clang', when="@:0.1.99", msg="No Darwin support for clang in older versions")
    conflicts('%clang platform=darwin', when="@:0.1.99", msg="No Darwin support for clang in older versions")

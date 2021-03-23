# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaCsgTutorials(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA coarse-graining tutorials.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/csg-tutorials/tarball/v1.4"
    git      = "https://github.com/votca/csg-tutorials.git"
    maintainers = ['junghans']

    version('master', branch='master')
    version('stable', branch='stable')
    version('2021', sha256='2b85c69007bb7d773529020e55fd82fed65651ee21eedccca9a801ab248ece97')
    version('1.6.4', sha256='34ef40db6b178a7f513f8a6f43e7caff6ecb498d66d7bf8bc44900bc7aea31dc')
    version('1.6.3', sha256='709582b978d84f9de09ae6c3ba4ed28daec886d4e0431bc7d19c7246bd65f0b1')
    version('1.6.2', sha256='7c25e76391f3ffdd15f8a91aeed2d3ce7377591f128ed4ae34b36eca20e5af8f')
    version('1.6.1', sha256='d8428c4a03ce42d88317045ec555af3defa022fd9a61f05e07b57c5577288c8c')
    version('1.6', sha256='54946c647724f1beb95942d47ec7f4cf7a95a59ec7268522693d5ec723585daf')
    version('1.5.1',   sha256='e35cea92df0e7d05ca7b449c1b5d84d887a3a23c7796abe3b84e4d6feec7faca')
    version('1.5',     sha256='03b841fb94129cf59781a7a5e3b71936c414aa9dfa17a50d7bc856d46274580c')
    version('1.4.1',   sha256='623724192c3a7d76b603a74a3326f181045f10f38b9f56dce754a90f1a74556e')
    version('1.4',     sha256='27d50acd68a9d8557fef18ec2b0c62841ae91c22275ab9afbd65c35e4dd5f719')

    for v in ["1.4", "1.4.1", "1.5", "1.5.1", "1.6", "1.6.1", "1.6.2",
              "1.6.3", "1.6.4", "2021", "master", "stable"]:
        depends_on('votca-csg@%s' % v, when="@%s:%s.0" % (v, v))
    depends_on("boost")

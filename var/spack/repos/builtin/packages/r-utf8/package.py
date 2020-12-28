# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUtf8(RPackage):
    """Process and print 'UTF-8' encoded international text
       (Unicode). Input, validate, normalize, encode, format, and display."""

    homepage = "https://cloud.r-project.org/package=utf8"
    url      = "https://cloud.r-project.org/src/contrib/utf8_1.1.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/utf8"

    version('1.1.4', sha256='f6da9cadfc683057d45f54b43312a359cf96ec2731c0dda18a8eae31d1e31e54')
    version('1.1.3', sha256='43b394c3274ba0f66719d28dc4a7babeb87187e766de8d8ca716e0548091440f')
    version('1.1.2', sha256='148517aadb75d82aba61f63afe2a30d254abebbdc7e32dd0830e12ff443915b9')
    version('1.1.1', sha256='0e30c824e43cdc0a3339f4688e3271737d02ea10768a46137e0e41936051cb3d')
    version('1.1.0', sha256='6a8ae2c452859800c3ef12993a55892588fc35df8fa1360f3d182ed97244dc4f')
    version('1.0.0', sha256='7562a80262cbc2017eee76c0d3c9575f240fab291f868a11724fa04a116efb80')

    depends_on('r@2.10:', type=('build', 'run'))

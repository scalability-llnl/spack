# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyApex(PythonPackage):
    """apex: Pyramid toolkit to add Velruse, Flash Messages,CSRF,
    ReCaptcha and Sessions."""

    homepage = "https://pypi.org/project/apex/"
    url      = "https://pypi.io/packages/source/a/apex/apex-0.9.10dev.tar.gz"

    version('0.9.10dev', sha256='48aa6d9e805e661e609161bd52e0d02d89a9a32f32dc29cde6c950df58129119')

    depends_on('py-setuptools', type='build')

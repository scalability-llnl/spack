# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySemanticVersion(PythonPackage):
    """This small python library provides a few tools to handle SemVer in
    Python. It follows strictly the 2.0.0 version of the SemVer scheme."""

    homepage = "https://github.com/rbarrois/python-semanticversion"
    url      = "https://pypi.io/packages/source/s/semantic_version/semantic_version-2.8.2.tar.gz"

    version('2.8.2', sha256='71c716e99086c44d068262b86e4775aa6db7fabee0743e4e33b00fbf6f672585')
    version('2.6.0', sha256='2a4328680073e9b243667b201119772aefc5fc63ae32398d6afafff07c4f54c0')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools@0.8:', type='build')

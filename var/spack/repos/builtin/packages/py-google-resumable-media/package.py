# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleResumableMedia(PythonPackage):
    """Utilities for Google Media Downloads and Resumable Uploads."""

    homepage = "https://github.com/GoogleCloudPlatform/google-resumable-media-python"
    url      = "https://pypi.io/packages/source/g/google-resumable-media/google-resumable-media-0.3.2.tar.gz"

    version('0.3.2', sha256='3e38923493ca0d7de0ad91c31acfefc393c78586db89364e91cb4f11990e51ba')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))

# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmartOpen(PythonPackage):
    """smart_open is a Python 2 & Python 3 library for efficient streaming of
       very large files from/to S3, HDFS, WebHDFS, HTTP, or local storage. It
       supports transparent, on-the-fly (de-)compression for a variety of
       different formats."""

    homepage = "https://github.com/piskvorky/smart_open"
    url      = "https://pypi.io/packages/source/s/smart_open/smart_open-1.10.0.tar.gz"

    version('1.10.0', sha256='bea5624c0c2e49987c227bdf3596573157eccd96fd1d53198856c8d53948fa2c')
    version('1.8.4',  sha256='788e07f035defcbb62e3c1e313329a70b0976f4f65406ee767db73ad5d2d04f9')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-boto3', type=('build', 'run'))
    depends_on('py-boto@2.3.2:', when='@1.8.4', type=('build', 'run'))
    depends_on('py-google-cloud-storage', when='@1.10:', type=('build', 'run'))
    depends_on('py-bz2file', when='^python@:2', type=('build', 'run'))

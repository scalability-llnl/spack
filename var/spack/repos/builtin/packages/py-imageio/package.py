# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImageio(PythonPackage):
    """ Imageio is a Python library that provides an easy interface
    to read and write a wide range of image data, including animated
    images, video, volumetric data, and scientific formats. It is
    cross-platform, runs on Python 2.7 and 3.4+, and is easy to install."""

    homepage = "http://imageio.github.io/"
    url      = "https://pypi.io/packages/source/i/imageio/imageio-2.3.0.tar.gz"

    version('2.5.0', sha256='42e65aadfc3d57a1043615c92bdf6319b67589e49a0aae2b985b82144aceacad')
    version('2.4.1', sha256='16b8077bc8a5fa7a58b3e744f7ecbb156d8c088132df31e0f4f546c98de3514a')
    version('2.3.0', sha256='c4fd5183c342d47fdc2e98552d14e3f24386021bbc3efedd1e3b579d7d249c07')

    # TODO: Add variants for plugins, and optional dependencies

    # Fix for python 2 if needed.
    depends_on('py-numpy',            type=('build', 'run'))
    depends_on('pil',                 type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools',       type='build')
    depends_on('ffmpeg',              type='run')

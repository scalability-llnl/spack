# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPip(PythonPackage):
    """The PyPA recommended tool for installing Python packages."""

    homepage = "https://pip.pypa.io/"
    url      = "https://pypi.io/packages/source/p/pip/pip-20.2.tar.gz"

    version('20.2',   sha256='912935eb20ea6a3b5ed5810dde9754fde5563f5ca9be44a8a6e5da806ade970b')
    version('19.3',   sha256='324d234b8f6124846b4e390df255cacbe09ce22791c3b714aa1ea6e44a4f2861')
    version('19.1.1', sha256='44d3d7d3d30a1eb65c7e5ff1173cdf8f7467850605ac7cc3707b6064bddd0958')
    version('19.0.3', sha256='6e6f197a1abfb45118dbb878b5c859a0edbdd33fd250100bc015b67fded4b9f2')
    version('18.1',   sha256='c0a292bd977ef590379a3f05d7b7f65135487b67470f6281289a94e015650ea1')
    version('10.0.1', sha256='f2bd08e0cd1b06e10218feaf6fef299f473ba706582eb3bd9d52203fdbd7ee68')
    version('9.0.1',  sha256='09f243e1a7b461f654c26a725fa373211bb7ff17a9300058b205c61658ca940d')

    depends_on('python@3.5:', when='@21:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', when='@19.2:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@18:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:', when='@10:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))

    # Most Python packages only require setuptools as a build dependency.
    # However, pip requires setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))

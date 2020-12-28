# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlake8(PythonPackage):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""

    homepage = "https://github.com/PyCQA/flake8"
    url      = "https://github.com/PyCQA/flake8/archive/3.7.8.tar.gz"

    version('3.8.2', sha256='ae9b00ddaa2bb7fa69796ac73ba7607fcf06d79a8b777fa12ba5abef1e770491')
    version('3.7.8',  sha256='201720797dc9691dd349819994e4a0bc281b70ee2ff77b0c928bb1d3c5aa9810')
    version('3.7.7',  sha256='b3f76b02351008dc772276e74b09dd3d4b5c567ff8c6ab573352cb8fd7007444')
    version('3.5.0', sha256='60ffe2fdacce4ebe7cadc30f310cf1edfd8ff654ef79525d90cf0756e69de44e')
    version('3.0.4', sha256='87a2b642900a569fc2f27ab3b79573e0d02d2fee7445c6abab84eb33dcb60365')
    version('2.5.4', sha256='ce03cc1acbe1726775ca57b40fab1d177550debb2f2f6b7a3c860541f3971cf5')

    extends('python', ignore='bin/(pyflakes|pycodestyle)')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-flake8 requires py-setuptools during runtime as well.
    depends_on('py-setuptools@30:', type=('build', 'run'))

    # Flake8 uses ranges for its dependencies to enforce a stable list of
    # error codes within each minor release:
    # http://flake8.pycqa.org/en/latest/faq.html#why-does-flake8-use-ranges-for-its-dependencies
    # http://flake8.pycqa.org/en/latest/internal/releases.html#releasing-flake8

    # Flake8 3.8.X
    depends_on('py-pycodestyle@2.6.0:2.6.999', when='@3.8.0:3.8.999', type=('build', 'run'))
    depends_on('py-pyflakes@2.2.0:2.2.999',    when='@3.8.0:3.8.999', type=('build', 'run'))

    # Flake8 3.7.X
    # FIXME @0.3.0:0.3.999 causes concretization to hang
    depends_on('py-entrypoints@0.3',           when='@3.7.0:3.8.999', type=('build', 'run'))
    depends_on('py-pyflakes@2.1.0:2.1.999',    when='@3.7.0:3.7.999', type=('build', 'run'))
    depends_on('py-pycodestyle@2.5.0:2.5.999', when='@3.7.0:3.7.999', type=('build', 'run'))
    depends_on('py-mccabe@0.6.0:0.6.999',      when='@3.7.0:3.8.999', type=('build', 'run'))

    # Flake8 3.5.X
    depends_on('py-pyflakes@1.5:1.6',     when='@3.5.0:3.5.999', type=('build', 'run'))
    depends_on('py-pycodestyle@2.0:2.4',  when='@3.5.0:3.5.999', type=('build', 'run'))
    depends_on('py-mccabe@0.6.0:0.6.999', when='@3.5.0:3.5.999', type=('build', 'run'))

    # Flake8 3.0.X
    depends_on('py-pyflakes@0.8.1:1.1,1.2.3:1.2.999', when='@3.0.0:3.0.999', type=('build', 'run'))
    depends_on('py-pycodestyle@2.0.0:2.0.999',        when='@3.0.0:3.0.999', type=('build', 'run'))
    depends_on('py-mccabe@0.5.0:0.5.999',             when='@3.0.0:3.0.999', type=('build', 'run'))

    # Flake8 2.5.X
    depends_on('py-pyflakes@0.8.1:1.0',               when='@2.5.0:2.5.999', type=('build', 'run'))
    depends_on('py-pycodestyle@1.5.7:1.5.999,1.6.3:', when='@2.5.0:2.5.999', type=('build', 'run'))
    depends_on('py-mccabe@0.2.1:0.4',                 when='@2.5.0:2.5.999', type=('build', 'run'))

    # Python version-specific backports
    depends_on('py-importlib-metadata', when='@3.8.0: ^python@:3.7', type=('build', 'run'))
    depends_on('py-enum34',             when='@3.0.0: ^python@:3.3', type=('build', 'run'))
    depends_on('py-typing',             when='@3.7.0: ^python@:3.4', type=('build', 'run'))
    depends_on('py-configparser',       when='@3.0.0: ^python@:3.1', type=('build', 'run'))
    depends_on('py-functools32',        when='@3.7.4: ^python@:3.1', type=('build', 'run'))

    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", 'setup.py', string=True)

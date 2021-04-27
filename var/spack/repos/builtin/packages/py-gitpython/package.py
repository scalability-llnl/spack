# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyGitpython(PythonPackage):
    """GitPython is a python library used to interact with Git repositories."""

    homepage = "http://gitpython.readthedocs.org"
    pypi = "GitPython/GitPython-3.1.12.tar.gz"

    version('3.1.12',  sha256='42dbefd8d9e2576c496ed0059f3103dcef7125b9ce16f9d5f9c834aed44a1dac')
    version('3.1.11',  sha256='befa4d101f91bad1b632df4308ec64555db684c360bd7d2130b4807d49ce86b8')
    version('3.1.10',  sha256='f488d43600d7299567b59fe41497d313e7c1253a9f2a8ebd2df8af2a1151c71d')
    version('3.1.9',  sha256='a03f728b49ce9597a6655793207c6ab0da55519368ff5961e4a74ae475b9fa8e')
    version('3.1.8',  sha256='080bf8e2cf1a2b907634761c2eaefbe83b69930c94c66ad11b65a8252959f912')
    version('3.1.7',  sha256='2db287d71a284e22e5c2846042d0602465c7434d910406990d5b74df4afb0858')
    version('3.1.6',  sha256='b54969b3262d4647f80ace8e9dd4e3f99ac30cc0f3e766415b349208f810908f')
    version('3.1.5',  sha256='90400ecfa87bac36ac75dfa7b62e83a02017b51759f6eef4494e4de775b2b4be')
    version('3.1.4',  sha256='fa98ce1f05805d59bbc3adb16c0780e5ca43b5ea9422feecf1cd0949a61d947e')
    version('3.1.3',  sha256='e107af4d873daed64648b4f4beb89f89f0cfbe3ef558fc7821ed2331c2f8da1a')
    version('3.1.2',  sha256='864a47472548f3ba716ca202e034c1900f197c0fb3a08f641c20c3cafd15ed94')
    version('3.1.1',  sha256='6d4f10e2aaad1864bb0f17ec06a2c2831534140e5883c350d58b4e85189dab74')
    version('3.1.0',  sha256='e426c3b587bd58c482f0b7fe6145ff4ac7ae6c82673fc656f489719abca6f4cb')
    version('3.0.9',  sha256='7e5df21bfef38505115ad92544fb379e6fedb2753f3b709174c4358cecd0cb97')

    depends_on('python@3.4:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-gitdb@4.0.1:4.999', type=('build', 'run'))

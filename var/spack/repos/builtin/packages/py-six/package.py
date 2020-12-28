# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySix(PythonPackage):
    """Python 2 and 3 compatibility utilities."""

    homepage = "https://pypi.python.org/pypi/six"
    url      = "https://pypi.io/packages/source/s/six/six-1.11.0.tar.gz"

    version('1.14.0', sha256='236bdbdce46e6e6a3d61a337c0f8b763ca1e8717c03b369e87a7ec7ce1319c0a')
    version('1.12.0', sha256='d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73')
    version('1.11.0', sha256='70e8a77beed4562e7f14fe23a786b54f6296e34344c23bc42f07b15018ff98e9')
    version('1.10.0', sha256='105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a')
    version('1.9.0',  sha256='e24052411fc4fbd1f672635537c3fc2330d9481b18c0317695b46259512c91d5')
    version('1.8.0',  sha256='047bbbba41bac37c444c75ddfdf0573dd6e2f1fbd824e6247bb26fa7d8fa3830')

    extends('python', ignore=r'bin/pytest')
    depends_on('py-setuptools', type='build')

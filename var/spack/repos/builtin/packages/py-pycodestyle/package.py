# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycodestyle(PythonPackage):
    """pycodestyle is a tool to check your Python code against some of the
    style conventions in PEP 8. Note: formerly called pep8."""

    homepage = "https://github.com/PyCQA/pycodestyle"
    url      = "https://github.com/PyCQA/pycodestyle/archive/2.0.0.tar.gz"

    version('2.6.0', sha256='08347fbc48cc92afd33117c1e8af9b99b292a4e5889f6b776f402e062fc39c97')
    version('2.5.0', sha256='a603453c07e8d8e15a43cf062aa7174741b74b4a27b110f9ad03d74d519173b5')
    version('2.3.1', sha256='e9fc1ca3fd85648f45c0d2e33591b608a17d8b9b78e22c5f898e831351bacb03')
    version('2.3.0', sha256='ac2a849987316521a56814b5618668d36cd5f3b04843803832a15b93b8383a50')
    version('2.2.0', sha256='aa663451c9de97d00eff396eeffe1095fd1597491341ca3c0be54983b25b1a7d')
    version('2.1.0', sha256='2190466d2b421da0d915b506eb690a6784feaef3ba33043665bf86581b02ccd9')
    version('2.0.0', sha256='7e65a888def0abc467fa2cf614b3f84a74a8991045a2adcf11e1c225d8798796')
    version('1.7.0', sha256='3f62d19b5cbcbdcb7810f967dcc2fbdd090256e090c32b457e2580a841d118ef')
    version('1.6.2', sha256='508bfd7d457046891bf4b8fbfc95ccac7995c37cdfdb3daf97bfeb7a13fa4c9c')
    version('1.6.1', sha256='3a910a0d0d998d4c3c2b8152a4816b98938b27cc73a4433c61202449706a73c8')
    version('1.6',   sha256='5e7bb5156af311079345b5e81f8154c3e1420d723150a6cba5a70245eb0d515a')
    version('1.5.7', sha256='9bf020638986f2e254823aee62cfd97e55ba08ad51503cd5ae26172c47f48401')
    version('1.5.6', sha256='9f164c1211854678b2cb269954bc8aac2dcfa142d40c99f7bab08f9344cf3241')
    version('1.5.5', sha256='e55204c5477a29eb094835ad6e83be292aa3e06be12e51f5b4cc67f38d0d61ba')
    version('1.5.4', sha256='bc234f7935a350c79c953421b01163db01010f39caeddfa8602ff54f76a6fd9e')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pycodestyle requires py-setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))

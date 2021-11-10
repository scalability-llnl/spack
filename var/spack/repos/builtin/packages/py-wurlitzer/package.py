# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWurlitzer(PythonPackage):
    """Capture C-level stdout/stderr pipes in Python via os.dup2."""

    homepage = "https://github.com/minrk/wurlitzer"
    url      = "https://github.com/minrk/wurlitzer/archive/refs/tags/3.0.2.tar.gz"
    maintainers = ['sethrj']

    version('3.0.2', sha256='c09508dbf8e1e53f8fcc703790887f446d8c08c705a8f14957ccfdb0dc17e8a0')

    depends_on('python+ctypes@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    # In some circumstances (unclear exactly what) Wurlitzer is unable to get
    # stdout/stderr pointers from ctypes, so it falls back to trying to use
    # cffi. If you encounter this, please add the dependency below.
    # depends_on('py-cffi', type='run', when='...????')

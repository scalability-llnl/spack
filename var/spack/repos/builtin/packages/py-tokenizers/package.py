# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyTokenizers(PythonPackage):
    """Fast and Customizable Tokenizers."""

    homepage = "https://github.com/huggingface/tokenizers"
    url      = "https://pypi.io/packages/source/t/tokenizers/tokenizers-0.6.0.tar.gz"

    version('0.6.0', sha256='1da11fbfb4f73be695bed0d655576097d09a137a16dceab2f66399716afaffac')
    version('0.5.2', sha256='b5a235f9c71d04d4925df6c4fa13b13f1d03f9b7ac302b89f8120790c4f742bc')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-rust', type='build')
    depends_on('rust@nightly', type='build')

    # TODO: This package currently requires internet access to install.
    # Also, a nightly or dev version of rust is required to build.
    # https://github.com/huggingface/tokenizers/issues/176
    # https://github.com/PyO3/pyo3/issues/5

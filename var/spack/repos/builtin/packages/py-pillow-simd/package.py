# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkg.builtin.py_pillow import PyPillowBase


class PyPillowSimd(PyPillowBase):
    """Pillow-SIMD is a SIMD-enabled fork of Pillow. It is usually 4-6x
    faster than the original Pillow in image processing benchmarks."""

    # See https://github.com/spack/spack/pull/15566
    _name = 'py-pillow-simd'
    homepage = "https://github.com/uploadcare/pillow-simd"
    url      = "https://pypi.io/packages/source/P/Pillow-SIMD/Pillow-SIMD-7.0.0.post3.tar.gz"

    version('7.0.0.post3', sha256='c27907af0e7ede1ceed281719e722e7dbf3e1dbfe561373978654a6b64896cb7')
    version('6.2.2.post1', sha256='d29b673ac80091797f1e8334458be307e4ac4ab871b0e495cfe56cb7b1d7704e')

    for ver in ['6.2.2.post1', '7.0.0.post3']:
        provides('pil@' + ver, when='@' + ver)

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_pillow import PyPillowBase


class PyPillowSimd(PyPillowBase):
    """Pillow-SIMD is a SIMD-enabled fork of Pillow. It is usually 4-6x
    faster than the original Pillow in image processing benchmarks."""

    # See https://github.com/spack/spack/pull/15566
    _name = "py-pillow-simd"
    homepage = "https://github.com/uploadcare/pillow-simd"
    pypi = "Pillow-SIMD/Pillow-SIMD-7.0.0.post3.tar.gz"

    version(
        "9.5.0.post1", sha256="8c89b85c4085532752625f2cc066a28547cebb98529acf932d5d84c1a7ab2abc"
    )
    version(
        "9.0.0.post1", sha256="918541cfaa90ba3c0e1bae5da31ba1b1f52b09c0009bd90183b787af4e018263"
    )
    version(
        "7.0.0.post3", sha256="c27907af0e7ede1ceed281719e722e7dbf3e1dbfe561373978654a6b64896cb7"
    )
    version(
        "6.2.2.post1", sha256="d29b673ac80091797f1e8334458be307e4ac4ab871b0e495cfe56cb7b1d7704e"
    )

    depends_on("c", type="build")  # generated

    for ver in ["6.2.2.post1", "7.0.0.post3", "9.0.0.post1", "9.5.0.post1"]:
        provides("pil@" + ver, when="@" + ver)

    conflicts("target=aarch64:")

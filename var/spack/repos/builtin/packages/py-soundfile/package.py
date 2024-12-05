# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySoundfile(PythonPackage):
    """SoundFile is an audio library based on libsndfile, CFFI and NumPy."""

    homepage = "https://github.com/bastibe/PySoundFile"
    pypi = "SoundFile/SoundFile-0.10.3.post1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.10.3.post1", sha256="490cff42650733d1832728b937fe99fa1802896f5ef4d61bcf78cf7ebecb107b"
    )

    variant("numpy", default=True, description="Support for processing audio data as numpy arrays")

    depends_on("py-setuptools", type="build")
    depends_on("py-cffi@1.0:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"), when="+numpy")
    depends_on("libsndfile", type="run")

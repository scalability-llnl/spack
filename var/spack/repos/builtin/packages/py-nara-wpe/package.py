# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNaraWpe(PythonPackage):
    """Background noise and signal reverberation due to reflections in an
    enclosure are the two main impairments in acoustic signal processing and
    far-field speech recognition. This work addresses signal dereverberation
    techniques based on WPE for speech recognition and other far-field
    applications. WPE is a compelling algorithm to blindly dereverberate
    acoustic signals based on long-term linear prediction."""

    homepage = "https://github.com/fgnt/nara_wpe"
    pypi = "nara_wpe/nara_wpe-0.0.7.tar.gz"

    license("MIT")

    version("0.0.7", sha256="7aa2edd5261e5d953e584e69a9233d60fc588fc8a4b7886c3ce43cc8ac8cd99b")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-soundfile", type=("build", "run"))
    depends_on("py-bottleneck", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))

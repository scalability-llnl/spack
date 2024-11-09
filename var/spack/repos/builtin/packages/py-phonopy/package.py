# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPhonopy(PythonPackage):
    """Phonopy is an open source package for phonon
    calculations at harmonic and quasi-harmonic levels."""

    homepage = "https://atztogo.github.io/phonopy/index.html"
    url = (
        "http://sourceforge.net/projects/phonopy/files/phonopy/phonopy-1.10/phonopy-1.10.0.tar.gz"
    )

    version("1.10.0", sha256="6b7c540bbbb033203c45b8472696db02a3a55913a0e5eb23de4dc9a3bee473f7")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))

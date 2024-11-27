# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurora(PythonPackage):
    """A Python Toolbox for Multimodal Neural Data Representation Analysis."""

    homepage = "https://github.com/ZitongLu1996/NeuroRA"
    pypi = "neurora/neurora-1.1.5.16.tar.gz"

    license("MIT")

    version("1.1.6.10", sha256="cdfed753b9d2e227cd15e3215fc0297ad5df0b131ef87a849e3fcec90788c514")
    version("1.1.6.9", sha256="052d826e17d6a40171d487b188bd68863e36e41e37740da5eec33562241e36ce")
    version("1.1.6.8", sha256="84aebe82ce0e8e99b306dcab7b5e15f85269862c379f16b8161dbab64e7d1dd2")
    version("1.1.6.1", sha256="97b2d1287f273a8db11dcaa623fc906b47ee7c4459e264a42b131e6a4f332916")
    version("1.1.5.16", sha256="5ae296a5baf658b67e9754a172f5fb321c2077007455f93db6bb2aaeb3e23cd7")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy@1.6.2:", type=("build", "run"))
    depends_on("py-mne", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-nilearn", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydeface(PythonPackage):
    """A script to remove facial structure from MRI images."""

    homepage = "http://poldracklab.org/"
    pypi = "pydeface/pydeface-2.0.2.tar.gz"
    git = "https://github.com/poldracklab/pydeface"

    license("MIT")

    version("2.0.2", sha256="662263072ccccff9929432568caf5c183075f7fbf8f9d5c170767c3202c78f36")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("py-nipype", type=("build", "run"))

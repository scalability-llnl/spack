# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH5sh(PythonPackage):
    """Shell-like environment for HDF5."""

    homepage = "https://github.com/sethrj/h5sh"
    pypi = "h5sh/h5sh-0.1.1.tar.gz"

    maintainers("sethrj")

    license("BSD-3-Clause")

    version("0.1.1", sha256="ccd8fed532d479d297baef044265100a4fb9cd119bce6f43270f2ee9f63a2183")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-h5py@2.7.1:", type=("build", "run"))
    depends_on("py-numpy@1.15:", type=("build", "run"))
    depends_on("py-prompt-toolkit@2:", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))

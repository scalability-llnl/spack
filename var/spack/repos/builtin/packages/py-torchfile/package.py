# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchfile(PythonPackage):
    """Mostly direct port of the torch7 Lua and C serialization
    implementation to Python, depending only on numpy (and the
    standard library: array and struct). Sharing of objects
    including torch.Tensors is preserved."""

    homepage = "https://github.com/bshillingford/python-torchfile"
    pypi = "torchfile/torchfile-0.1.0.tar.gz"
    # license = "BSD-3-Clause"

    version("0.1.0", sha256="a53dfe134b737845a9f2cb24fe0585317874f965932cebdb0439d13c8da4136e")

    depends_on("python@2.7:2,3.4:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))

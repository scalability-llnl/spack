# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDxfile(PythonPackage):
    """Scientific Data Exchange [A1] is a set of guidelines for storing scientific
    data and metadata in a Hierarchical Data Format 5 [B6] file."""

    homepage = "https://github.com/data-exchange/dxfile"
    url = "https://github.com/data-exchange/dxfile/archive/v0.4.tar.gz"

    version("0.4", sha256="b7729eebdc7c99a66a8b339fc10019aa8565e02bd12708540fb3f47935f004c7")

    depends_on("py-setuptools", type="build")
    depends_on("py-h5py", type=("build", "run"))

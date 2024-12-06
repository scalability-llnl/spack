# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLazyLoader(PythonPackage):
    """lazy_loader makes it easy to load subpackages and functions on demand."""

    homepage = "https://scientific-python.org/specs/spec-0001/"
    pypi = "lazy_loader/lazy_loader-0.1.tar.gz"

    license("BSD-3-Clause")

    version("0.4", sha256="47c75182589b91a4e1a85a136c074285a5ad4d9f39c63e0d7fb76391c4574cd1")
    version("0.3", sha256="3b68898e34f5b2a29daaaac172c6555512d0f32074f147e2254e4a6d9d838f37")
    version("0.1", sha256="77ce7f2737ebabf9c0ff73b4a99c947876d74d24c2f026544e32246ecca5feca")

    depends_on("py-setuptools@61.2:", when="@0.4:", type="build")
    depends_on("py-packaging", when="@0.4:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-flit-core@3.8:3", when="@0.3", type="build")
    depends_on("py-flit-core@3.7:3", when="@0.1", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultipledispatch(PythonPackage):
    """A relatively sane approach to multiple dispatch in Python."""

    homepage = "https://multiple-dispatch.readthedocs.io/"
    url = "https://github.com/mrocklin/multipledispatch/archive/0.6.0.tar.gz"

    license("BSD-3-Clause")

    version("0.6.0", sha256="649f6e61b8a6ce581c75f32365c926b55495c01b8177135408b83aa03886cde0")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))

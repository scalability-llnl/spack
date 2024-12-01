# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeepdiff(PythonPackage):
    """Deep Difference and Search of any Python object/data.."""

    homepage = "https://github.com/seperman/deepdiff"
    pypi = "deepdiff/deepdiff-5.6.0.tar.gz"

    license("MIT")

    version("6.3.0", sha256="6a3bf1e7228ac5c71ca2ec43505ca0a743ff54ec77aa08d7db22de6bc7b2b644")
    version("5.6.0", sha256="e3f1c3a375c7ea5ca69dba6f7920f9368658318ff1d8a496293c79481f48e649")

    depends_on("py-setuptools", type="build")
    depends_on("py-ordered-set@4.0.2:4.1", when="@6:", type=("build", "run"))
    depends_on("py-ordered-set@4.0.2", when="@:5", type=("build", "run"))

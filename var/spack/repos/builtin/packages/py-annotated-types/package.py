# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnnotatedTypes(PythonPackage):
    """Reusable constraint types to use with typing.Annotated."""

    homepage = "https://github.com/annotated-types/annotated-types"
    pypi = "annotated_types/annotated_types-0.7.0.tar.gz"

    license("MIT", checked_by="wdconinc")

    version("0.7.0", sha256="aff07c09a53a08bc8cfccb9c85b05f1aa9a2a6f23728d790723543408344ce89")

    depends_on("py-hatchling", type="build")
    depends_on("py-typing-extensions@4.0.0:", when="^python@:3.8", type=("build", "run"))

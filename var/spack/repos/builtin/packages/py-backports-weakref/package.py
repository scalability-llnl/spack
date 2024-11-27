# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsWeakref(PythonPackage):
    """Backports of new features in Python's weakref module"""

    homepage = "https://github.com/PiDelport/backports.weakref"
    pypi = "backports.weakref/backports.weakref-1.0.post1.tar.gz"

    license("PSF-2.0")

    version(
        "1.0.post1",
        sha256="bc4170a29915f8b22c9e7c4939701859650f2eb84184aee80da329ac0b9825c2",
        preferred=True,
    )
    version("1.0rc1", sha256="8813bf712a66b3d8b85dc289e1104ed220f1878cf981e2fe756dfaabe9a82892")

    depends_on("py-setuptools", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBagitProfile(PythonPackage):
    """A simple Python module for validating BagIt profiles."""

    homepage = "https://github.com/bagit-profiles/bagit-profiles-validator"
    pypi = "bagit-profile/bagit_profile-1.3.1.tar.gz"

    license("Unlicense")

    version("1.3.1", sha256="57798cdcf98b32a413edb29382d85f4f8c44d3204940d7e12d84998521a98c3f")

    depends_on("python@2.7,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-bagit", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPatchNg(PythonPackage):
    """Library to parse and apply unified diffs."""

    homepage = "https://github.com/conan-io/python-patch"
    pypi = "patch-ng/patch-ng-1.17.4.tar.gz"

    license("MIT")

    version("1.17.4", sha256="627abc5bd723c8b481e96849b9734b10065426224d4d22cd44137004ac0d4ace")

    depends_on("py-setuptools", type="build")

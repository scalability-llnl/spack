# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJsondiff(PythonPackage):
    """Diff JSON and JSON-like structures in Python."""

    homepage = "https://github.com/ZoomerAnalytics/jsondiff"
    pypi = "jsondiff/jsondiff-1.2.0.tar.gz"

    license("MIT")

    version("1.2.0", sha256="34941bc431d10aa15828afe1cbb644977a114e75eef6cc74fb58951312326303")

    depends_on("py-setuptools", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRtoml(PythonPackage):
    """A better TOML library for python implemented in rust."""

    homepage = "https://github.com/samuelcolvin/rtoml"
    pypi = "rtoml/rtoml-0.9.0.tar.gz"

    license("MIT")

    version("0.9.0", sha256="113f2e133d152d9424269c475b4a7d0679987078b543e88fcb16c870dc2c460d")

    depends_on("rust", type="build")
    depends_on("py-maturin@0.13", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWstool(PythonPackage):
    """A tool for managing a workspace of multiple heterogenous SCM
    repositories."""

    homepage = "https://wiki.ros.org/wstool"
    pypi = "wstool/wstool-0.1.17.tar.gz"

    version("0.1.17", sha256="c79b4f110ef17004c24972d742d2c5f606b0f6b424295e7ed029a48e857de237")

    depends_on("py-setuptools", type="build")
    depends_on("py-vcstools@0.1.38:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))

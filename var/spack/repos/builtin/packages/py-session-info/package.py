# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySessionInfo(PythonPackage):
    """session_info outputs version information for modules
    loaded in the current session, Python, and the OS."""

    homepage = "https://gitlab.com/joelostblom/session_info"
    pypi = "session_info/session_info-1.0.0.tar.gz"

    version("1.0.0", sha256="3cda5e03cca703f32ae2eadbd6bd80b6c21442cfb60e412c21cb8ad6d5cbb6b7")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-stdlib-list", type=("build", "run"))

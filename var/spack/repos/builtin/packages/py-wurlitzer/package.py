# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWurlitzer(PythonPackage):
    """Capture C-level stdout/stderr pipes in Python via os.dup2."""

    pypi = "wurlitzer/wurlitzer-3.0.2.tar.gz"

    maintainers("sethrj")

    license("MIT")

    version("3.0.2", sha256="36051ac530ddb461a86b6227c4b09d95f30a1d1043de2b4a592e97ae8a84fcdf")

    depends_on("python+ctypes@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    # In some circumstances (unclear exactly what) Wurlitzer is unable to get
    # stdout/stderr pointers from ctypes, so it falls back to trying to use
    # cffi. If you encounter this, please add the dependency below.
    # depends_on('py-cffi', type='run', when='...????')

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFluflLock(PythonPackage):
    """NFS-safe file locking with timeouts for POSIX and Windows"""

    homepage = "https://fluflock.readthedocs.io"
    pypi = "flufl.lock/flufl.lock-5.0.4.tar.gz"

    license("Apache-2.0")

    version("5.0.4", sha256="09ffef831d57c4d182e398e97bb74ad8c8ffbd1710175a5a0b0f057095db12f1")
    version("5.0.3", sha256="94df161caa489d74afc26df8c0b640770923ecc0c6c5d331fbeabe7b91d306cb")
    version("3.2", sha256="a8d66accc9ab41f09961cd8f8db39f9c28e97e2769659a3567c63930a869ff5b")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-atpublic", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))

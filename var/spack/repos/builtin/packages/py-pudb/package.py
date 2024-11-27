# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPudb(PythonPackage):
    """Full-screen console debugger for Python"""

    homepage = "https://mathema.tician.de/software/pudb"
    pypi = "pudb/pudb-2017.1.1.tar.gz"

    license("MIT")

    version("2017.1.1", sha256="87117640902c5f602c8517d0167eb5c953a5bdede97975ba29ff17e3d570442c")
    version("2016.2", sha256="e958d7f7b1771cf297714e95054075df3b2a47455d7a740be4abbbd41289505a")

    # Most Python packages only require setuptools as a build dependency.
    # However, pudb requires setuptools during runtime as well.
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-urwid@1.1.1:", type=("build", "run"))
    depends_on("py-pygments@1.0:", type=("build", "run"))

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyScoop(PythonPackage):
    """SCOOP (Scalable COncurrent Operations in Python) is a distributed
    task module allowing concurrent parallel programming on various
    environments, from heterogeneous grids to supercomputers."""

    homepage = "https://github.com/soravux/scoop"
    pypi = "scoop/scoop-0.7.1.1.tar.gz"

    license("LGPL-3.0-only")

    version("0.7.1.1", sha256="d8b6444c7bac901171e3327a97e241dde63f060354e162a65551fd8083ca62b4")

    depends_on("py-setuptools", type="build")
    depends_on("py-greenlet@0.3.4:", type=("build", "run"))
    depends_on("py-pyzmq@13.1.0:", type=("build", "run"))

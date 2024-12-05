# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySshtunnel(PythonPackage):
    """Pure python SSH tunnels."""

    homepage = "https://github.com/pahaz/sshtunnel"
    pypi = "sshtunnel/sshtunnel-0.1.5.tar.gz"

    license("MIT")

    version("0.1.5", sha256="c813fdcda8e81c3936ffeac47cb69cfb2d1f5e77ad0de656c6dab56aeebd9249")

    depends_on("py-setuptools", type="build")
    depends_on("py-paramiko@1.15.2:", type=("build", "run"))

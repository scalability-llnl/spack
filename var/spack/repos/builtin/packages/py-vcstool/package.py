# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyVcstool(PythonPackage):
    """vcstool enables batch commands on multiple different vcs repositories.

    Currently it supports git, hg, svn and bzr."""

    homepage = "https://github.com/dirk-thomas/vcstool"
    pypi = "vcstool/vcstool-0.2.15.tar.gz"

    version("0.2.15", sha256="b1fce6fcef7b117b245a72dc8658a128635749d01dc7e9d1316490f89f9c2fde")

    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHacking(PythonPackage):
    """OpenStack Hacking Guideline Enforcement."""

    homepage = "https://docs.openstack.org/hacking/latest/"
    pypi = "hacking/hacking-1.1.0.tar.gz"

    version("1.1.0", sha256="23a306f3a1070a4469a603886ba709780f02ae7e0f1fc7061e5c6fb203828fee")

    depends_on("py-setuptools", type="build")

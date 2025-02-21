# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVcversioner(PythonPackage):
    """Vcversioner: Take version numbers from version control."""

    homepage = "https://github.com/habnabit/vcversioner"
    pypi = "vcversioner/vcversioner-2.16.0.0.tar.gz"

    license("ISC")

    version("2.16.0.0", sha256="dae60c17a479781f44a4010701833f1829140b1eeccd258762a74974aa06e19b")

    depends_on("py-setuptools", type="build")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyfiglet(PythonPackage):
    """pyfiglet is a full port of FIGlet (http://www.figlet.org/)
    into purepython. It takes ASCII text and renders it in ASCII
    art font."""

    homepage = "https://github.com/pwaller/pyfiglet"
    pypi = "pyfiglet/pyfiglet-0.7.tar.gz"

    license("MIT")

    version("0.8.post1", sha256="c6c2321755d09267b438ec7b936825a4910fec696292139e664ca8670e103639")
    version("0.8.post0", sha256="2994451ea67c77cd97f81f52087ccae6921d78d9402920995419893a979b5ace")
    version("0.7.6", sha256="97d59651b40da6ddf7e961157c480a7a04b48214d8c7231adc8c15e43aa5d722")
    version("0.7.5", sha256="446194e1fc3257ffc8024eafd3b486394847597f6210278d76bd582850205e12")

    depends_on("py-setuptools", type=("build", "run"))

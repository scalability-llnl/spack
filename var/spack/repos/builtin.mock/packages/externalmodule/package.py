# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Externalmodule(Package):
    homepage = "http://somewhere.com"
    url = "http://somewhere.com/module-1.0.tar.gz"

    version("1.0", md5="1234567890abcdef1234567890abcdef")

    depends_on("externalprereq")

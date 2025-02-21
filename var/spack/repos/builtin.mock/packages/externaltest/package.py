# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Externaltest(Package):
    homepage = "http://somewhere.com"
    url = "http://somewhere.com/test-1.0.tar.gz"

    version("1.0", md5="1234567890abcdef1234567890abcdef")

    depends_on("stuff")
    depends_on("externaltool")

    def install(self, spec, prefix):
        touch(join_path(prefix, "an_installation_file"))

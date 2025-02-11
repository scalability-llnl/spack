# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Turnserver(AutotoolsPackage):
    """coturn TURN server project."""

    homepage = "https://github.com/coturn/coturn"
    url = "https://github.com/coturn/coturn/archive/4.6.2.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("4.6.2", sha256="408bf7fde455d641bb2a23ba2df992ea0ae87b328de74e66e167ef58d8e9713a")
    version(
        "4.5.1.3",
        sha256="408bf7fde455d641bb2a23ba2df992ea0ae87b328de74e66e167ef58d8e9713a",
        url="https://coturn.net/turnserver/v4.5.1.3/turnserver-4.5.1.3.tar.gz",
    )

    depends_on("c", type="build")

    depends_on("libevent")

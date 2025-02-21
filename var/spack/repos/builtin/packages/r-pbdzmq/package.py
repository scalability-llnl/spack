# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RPbdzmq(RPackage):
    """Programming with Big Data -- Interface to 'ZeroMQ'.

    'ZeroMQ' is a well-known library for high-performance asynchronous
    messaging in scalable, distributed applications. This package provides high
    level R wrapper functions to easily utilize 'ZeroMQ'. We mainly focus on
    interactive client/server programming frameworks. For convenience, a
    minimal 'ZeroMQ' library (4.1.0 rc1) is shipped with 'pbdZMQ', which can be
    used if no system installation of 'ZeroMQ' is available. A few wrapper
    functions compatible with 'rzmq' are also provided."""

    cran = "pbdZMQ"

    license("GPL-3.0-or-later")

    version("0.3-11", sha256="da7e204d857370201f75a05fbd808a2f409d440cc96855bb8f48f4a5dd75405b")
    version("0.3-9", sha256="d033238d0a9810581f6b40c7c75263cfc495a585653bbff98e957c37954e0fb6")
    version("0.3-8", sha256="eded4ccf6ee54a59e06061f1c6e67a8ec36e03c6ab2318af64446d8f95505465")
    version("0.3-7", sha256="df2d2be14b2f57a64d76cdda4c01fd1c3d9aa12221c63524c01c71849df11808")
    version("0.3-6", sha256="9944c8c44221aed1dbd7763ad9ec52c0ad2611d37bee25971ca16f02e8e8c37b")
    version("0.3-4", sha256="07794bd6858e093f8b6b879ddd5ab0195449b47a41b70cab2f60603f0a53b129")
    version("0.3-3", sha256="ae26c13400e2acfb6463ff9b67156847a22ec79f3b53baf65119efaba1636eca")
    version("0.3-2", sha256="ece2a2881c662f77126e4801ba4e01c991331842b0d636ce5a2b591b9de3fc37")
    version("0.2-4", sha256="bfacac88b0d4156c70cf63fc4cb9969a950693996901a4fa3dcd59949ec065f6")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@0.2-6:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.3-4:")
    depends_on("libzmq@4.0.4:")

    depends_on("r-r6", type=("build", "run"), when="@:0.2-6")

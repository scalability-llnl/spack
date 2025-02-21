# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRzmq(RPackage):
    """R Bindings for 'ZeroMQ'.

    Interface to the 'ZeroMQ' lightweight messaging kernel (see
    <http://www.zeromq.org/> for more information)."""

    cran = "rzmq"

    license("GPL-3.0-only")

    version("0.9.13", sha256="8d603543b23a0b78352b4995c90c03d00686fef1d7a25004b66690191fb463f1")
    version("0.9.8", sha256="815a7eb502b1da3a84246b2dfb6594ca3f241a8675783e6bcdbbf9c952ec1c53")
    version("0.9.7", sha256="5f47b67b75fd4a230780406f7a55a3708ce8c014cff755a809a6bfa1a6925a45")
    version("0.9.6", sha256="80a3fc6eb6f7851224c4cd5e219ca4db0286551ad429359d4df853ccb9234316")
    version("0.9.4", sha256="03fbda756d823c11fba359b94a6213c3440e61973331668eaac35779717f73ad")
    version("0.7.7", sha256="bdbaf77a0e04c5b6d6ce79ab2747848a5044355eed2e2c4d39c4ba16f97dc83d")

    depends_on("r@3.1.0:", type=("build", "run"), when="@0.9.0:")
    depends_on("libzmq@3.0.0:")

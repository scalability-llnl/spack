# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFutureApply(RPackage):
    """Apply Function to Elements in Parallel using Futures.

    Implementations of apply(), by(), eapply(), lapply(), Map(), mapply(),
    replicate(), sapply(), tapply(), and vapply() that can be resolved using
    any future-supported backend, e.g. parallel on the local machine or
    distributed on a compute cluster. These future_*apply() functions come with
    the same pros and cons as the corresponding base-R *apply() functions but
    with the additional feature of being able to be processed via the future
    framework."""

    cran = "future.apply"

    version("1.11.2", sha256="f4a635b0fa5e0d826d2f8da6bc1fa5bb055e640c29a85c644931d08ab2d81387")
    version("1.10.0", sha256="dee92dd84812fe8c55064c0f0e6d806c0c29848b5a5fc4a7725d6a4b623e94aa")
    version("1.9.1", sha256="4f22ccd5caa62077581c6adc4d35543451e547220270aed3f1abcbaa6a202133")
    version("1.9.0", sha256="6166c1c5ce30b9745059c3d30c8110f7c1d51871e58aa414f195cb1f91c467f5")
    version("1.8.1", sha256="0d5bc3cb0289665bb27ae4ccad51fcc5ebf6dca46872b0a4e57790b9dc0aa6c7")
    version("1.7.0", sha256="2ffa6adb55f239918ce9679b7eac8dcc4bf2e6bed35c9cbedf4bf90d906345db")
    version("1.3.0", sha256="6374eca49bb81e05c013509c8e324cf9c5d023f9f8217b29ce7b7e12025ca371")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-future@1.13.0:", type=("build", "run"))
    depends_on("r-future@1.17.0:", type=("build", "run"), when="@1.7.0:")
    depends_on("r-future@1.21.0:", type=("build", "run"), when="@1.8.1:")
    depends_on("r-future@1.22.1:", type=("build", "run"), when="@1.9.0:")
    depends_on("r-future@1.27.0:", type=("build", "run"), when="@1.9.1:")
    depends_on("r-future@1.28.0:", type=("build", "run"), when="@1.10.0:")
    depends_on("r-globals@0.12.4:", type=("build", "run"))
    depends_on("r-globals@0.12.5:", type=("build", "run"), when="@1.7.0:")
    depends_on("r-globals@0.14.0:", type=("build", "run"), when="@1.8.1:")
    depends_on("r-globals@0.16.1:", type=("build", "run"), when="@1.9.1:")

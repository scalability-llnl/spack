# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXts(RPackage):
    """eXtensible Time Series.

    Provide for uniform handling of R's different time-based data classes by
    extending zoo, maximizing native format information preservation and
    allowing for user level customization and extension, while simplifying
    cross-class interoperability."""

    cran = "xts"

    license("GPL-2.0-or-later")

    version("0.14.0", sha256="d28b16eefa9876a815bad3fc204779c197e3a0d7796b8dae8856fe153f5fcfd9")
    version("0.13.1", sha256="2c3907c6d0162e48d1898647105bbb32cfe0cb005788481a64ee675a941d825d")
    version("0.13.0", sha256="188e4d1d8c3ec56a544dfb9da002e8aac80b9303d0a5a1f62ff0e960aeef9674")
    version("0.12.2", sha256="9c287ceaeb758ff4c9596be6a688db5683d50b45e7610e6d068891ca10dca743")
    version("0.12.1", sha256="d680584af946fc30be0b2046e838cff7b3a65e00df1eadba325ca5e96f3dca2c")
    version("0.11-2", sha256="12772f6a66aab5b84b0665c470f11a3d8d8a992955c027261cfe8e6077ee13b8")
    version("0.9-7", sha256="f11f7cb98f4b92b7f6632a2151257914130880c267736ef5a264b5dc2dfb7098")

    depends_on("r@3.6.0:", type=("build", "run"), when="@0.13.0:")

    depends_on("r-zoo@1.7-12:", type=("build", "run"))

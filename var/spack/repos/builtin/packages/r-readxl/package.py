# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReadxl(RPackage):
    """Read Excel Files.

    Import excel files into R. Supports '.xls' via the embedded 'libxls' C
    library <https://sourceforge.net/projects/libxls/> and '.xlsx' via the
    embedded 'RapidXML' C++ library <https://rapidxml.sourceforge.net>. Works
    on Windows, Mac and Linux without external dependencies."""

    cran = "readxl"

    license("MIT")

    version("1.4.3", sha256="7efebbcdefeb8523633db62b3eeb6ea2e4e81e3d010d8b2adb134011c09a5948")
    version("1.4.2", sha256="387304e2c5be0dca4861ec0232f0d92cc1882b660ca917f8f2a8a4ae858aba11")
    version("1.4.1", sha256="f6bebb7f940fb21baacd60345b7075c77eb1d026466c55e6a36148de680da1fa")
    version("1.4.0", sha256="ab9239c249f79b649f7665a612b3dbf4b774ab633115e6dee41091a8cb2491f7")
    version("1.3.1", sha256="24b441713e2f46a3e7c6813230ad6ea4d4ddf7e0816ad76614f33094fbaaaa96")
    version("1.3.0", sha256="8379d1026dcfc662d073eb1c69ed1d90aa6439d6cb3c6fc1b5d1db4f51b3fadc")
    version("1.1.0", sha256="b63d21fc6510acb373e96deaec45e966a523ec75cbec75a089529297ed443116")
    version("1.0.0", sha256="fbd62f07fed7946363698a57be88f4ef3fa254ecf456ef292535849c787fc7ad")

    depends_on("r@3.4:", type=("build", "run"), when="@1.4.0:")
    depends_on("r@3.5:", type=("build", "run"), when="@1.4.2:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.4.3:")
    depends_on("r-cellranger", type=("build", "run"))
    depends_on("r-tibble@1.3.1:", type=("build", "run"))
    depends_on("r-tibble@2.0.1:", type=("build", "run"), when="@1.4.0:")
    depends_on("r-cpp11@0.4.0:", type=("build", "run"), when="@1.4.0:")
    depends_on("r-progress", type=("build", "run"), when="@1.2.0:")

    depends_on("r-rcpp@0.12.18:", type=("build", "run"), when="@:1.3.1")

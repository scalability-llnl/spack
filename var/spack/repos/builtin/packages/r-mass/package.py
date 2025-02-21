# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMass(RPackage):
    """Support Functions and Datasets for Venables and Ripley's MASS.

    Functions and datasets to support Venables and Ripley, "Modern Applied
    Statistics with S" (4th edition, 2002)."""

    cran = "MASS"

    version("7.3-61", sha256="3144c8bf579dd7b7c47c259728c27f53f53e294e7ed307da434dfd144e800a90")
    version("7.3-59", sha256="454200bec7a52835fbb7f9fe8e01a7aaa728b3ab87b068fc6d900e01c930da5a")
    version("7.3-58.1", sha256="f704e4e2fb131740d023ae1755c925c2e684886a3061b08e26397135f1231420")
    version("7.3-57", sha256="bd8b880105bc1aadb2db699086f74bd92a8611287979a24243187f9d80795a8d")
    version("7.3-55", sha256="65299cbc8f3fd5e09cb3535eabcb3faad2308e01d5ba9422145cc04d7d0c31a4")
    version("7.3-54", sha256="b800ccd5b5c2709b1559cf5eab126e4935c4f8826cf7891253432bb6a056e821")
    version("7.3-53", sha256="41824e70ada302a620226c0f17b1b2c880c6d1a3a100b53bd6df8e8c97e64b38")
    version("7.3-51.5", sha256="464c0615cef01820cde2bb8457e81575d6755ae9b3ac99f3bfaaac47d43d15cc")
    version("7.3-51.4", sha256="844270a2541eaed420871dfb61d681aa67ee57126645fb6b144b436c25698eeb")
    version("7.3-51.3", sha256="5b0e0e7704d43a94b08dcc4b3fe600b9723d1b3e446dd393e82d39ddf66608b6")
    version("7.3-47", sha256="ed44cdabe84fff3553122267ade61d5cc68071c435f7645d36c8f2e4e9f9c6bf")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@3.3.0:", type=("build", "run"), when="@7.3-55:")
    depends_on("r@4.2.0:", type=("build", "run"), when="@7.3-59:")
    depends_on("r@4.4.0:", type=("build", "run"), when="@7.3-60.1:")

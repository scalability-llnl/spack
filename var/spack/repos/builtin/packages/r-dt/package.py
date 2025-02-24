# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDt(RPackage):
    """A Wrapper of the JavaScript Library 'DataTables'.

    Data objects in R can be rendered as HTML tables using the JavaScript
    library 'DataTables' (typically via R Markdown or Shiny). The 'DataTables'
    library has been included in this R package. The package name 'DT' is an
    abbreviation of 'DataTables'."""

    cran = "DT"

    license("Apache-2.0")

    version("0.33", sha256="e145dadb1ce3db7c837f4313a8b5615b5b8ae63063ec2df93e528529717b27b8")
    version("0.27", sha256="e32fdccd2be430933cff88a9ce79045bfdbe3e08e0cd8d15037445808613289a")
    version("0.26", sha256="c412932be126d44f415559258e1d65adc0e84c3dfb9a70ce3196a2f877f7030c")
    version("0.25", sha256="0dfc8713062e1fe4e0428936367f35a0a41616c27b6d9b002bdfda58091c442b")
    version("0.23", sha256="360ae2fcb1141125a1b16448570fc37d14c4dd3f78a872c26df4fda1787cdc70")
    version("0.20", sha256="c66d7f49ec101fdbb91c6d26c06fb1373f9ebdefe29fe99f2ae1a641220aba9f")
    version("0.17", sha256="e3430292421dcc2b6ad5f2deda729f0603da4eb31f86d071833e6e11abf3fb56")
    version("0.13", sha256="79a073fe96980ce150d790ab76133c9e80bd463270c34d149c03934a622d63b5")
    version("0.8", sha256="90195054148806cf31c7db5c41f72d5389c75adc0b1183606a9babd2c6ae8e21")
    version("0.7", sha256="1de3f170deccd9e3aaefc057dd87c498e3b3f7f88eff645cf165ac34ffe3de2c")
    version("0.6", sha256="2ed68e9d161559171fa74b6105eee87b98acf755eae072b38ada60a83d427916")
    version("0.4", sha256="3daa96b819ca54e5fbc2c7d78cb3637982a2d44be58cea0683663b71cfc7fa19")
    version("0.3", sha256="ef42b24c9ea6cfa1ce089687bf858d773ac495dc80756d4475234e979bd437eb")
    version("0.2", sha256="a1b7f9e5c31a241fdf78ac582499f346e915ff948554980bbc2262c924b806bd")
    version("0.1", sha256="129bdafededbdcc3279d63b16f00c885b215f23cab2edfe33c9cbe177c8c4756")

    depends_on("r-htmltools@0.3.6:", type=("build", "run"))
    depends_on("r-htmlwidgets@1.3:", type=("build", "run"))
    depends_on("r-httpuv", type=("build", "run"), when="@0.29:")
    depends_on("r-jsonlite@0.9.16:", type=("build", "run"), when="@0.8:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-crosstalk", type=("build", "run"))
    depends_on("r-jquerylib", type=("build", "run"), when="@0.19:")
    depends_on("r-promises", type=("build", "run"), when="@0.5:")

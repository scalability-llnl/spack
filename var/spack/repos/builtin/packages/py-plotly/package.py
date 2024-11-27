# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlotly(PythonPackage):
    """An interactive, browser-based graphing library for Python"""

    homepage = "https://plot.ly/python/"
    pypi = "plotly/plotly-2.2.0.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("5.20.0", sha256="bf901c805d22032cfa534b2ff7c5aa6b0659e037f19ec1e0cca7f585918b5c89")
    version("5.19.0", sha256="5ea91a56571292ade3e3bc9bf712eba0b95a1fb0a941375d978cc79432e055f4")
    version("5.18.0", sha256="360a31e6fbb49d12b007036eb6929521343d6bee2236f8459915821baefa2cbb")
    version("5.17.0", sha256="290d796bf7bab87aad184fe24b86096234c4c95dcca6ecbca02d02bdf17d3d97")
    version("5.16.1", sha256="295ac25edeb18c893abb71dcadcea075b78fd6fdf07cee4217a4e1009667925b")
    version("5.15.0", sha256="822eabe53997d5ebf23c77e1d1fcbf3bb6aa745eb05d532afd4b6f9a2e2ab02f")
    version("5.14.1", sha256="bcac86d7fcba3eff7260c1eddc36ca34dae2aded10a0709808446565e0e53b93")
    version("5.2.2", sha256="809f0674a7991daaf4f287964d617d24e9fa44463acd5a5352ebd874cfd98b07")
    version("2.2.0", sha256="ca668911ffb4d11fed6d7fbb12236f8ecc6a7209db192326bcb64bdb41451a58")

    depends_on("python@3.6:3.11", when="@5.2.2:5.18.0", type=("build", "run"))
    depends_on("python@3.8:3.11", when="@5.19.0:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@40.8.0:", when="@5.14.1:", type="build")
    depends_on("py-jupyterlab@3", when="@5:", type="build")
    depends_on("py-six", when="@:5.2.2", type=("build", "run"))

    depends_on("py-pytz", when="@:2.2.0", type=("build", "run"))
    depends_on("py-decorator@4.0.6:", when="@:2.2.0", type=("build", "run"))
    depends_on("py-nbformat@4.2.0:", when="@:2.2.0", type=("build", "run"))
    depends_on("py-requests", when="@:2.2.0", type=("build", "run"))

    depends_on("py-tenacity@6.2.0:", when="@5.2.2:", type=("build", "run"))
    depends_on("py-packaging", when="@5.14.1:", type=("build", "run"))

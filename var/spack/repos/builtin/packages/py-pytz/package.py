# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytz(PythonPackage):
    """World timezone definitions, modern and historical."""

    homepage = "https://pythonhosted.org/pytz"
    pypi = "pytz/pytz-2019.3.tar.gz"
    git = "https://github.com/stub42/pytz.git"

    license("MIT")

    version("2024.2", sha256="2aa355083c50a0f93fa581709deac0c9ad65cca8a9e9beac660adcbd493c798a")
    version("2023.3", sha256="1d8ce29db189191fb55338ee6d0387d82ab59f3d00eac103412d64e0ebd0c588")
    version("2022.2.1", sha256="cea221417204f2d1a2aa03ddae3e867921971d0d76f14d87abb4414415bbdcf5")
    version("2021.3", sha256="acad2d8b20a1af07d4e4c9d2e9285c5ed9104354062f275f3fcd88dcef4f1326")
    version("2021.1", sha256="83a4a90894bf38e243cf052c8b58f381bfe9a7a483f6a9cab140bc7f702ac4da")
    version("2020.1", sha256="c35965d010ce31b23eeb663ed3cc8c906275d6be1a34393a1d73a41febf4a048")
    version("2019.3", sha256="b02c06db6cf09c12dd25137e563b31700d3b80fcc4ad23abb7a315f2789819be")
    version("2019.1", sha256="d747dd3d23d77ef44c6a3526e274af6efeb0a6f1afd5a69ba4d5be4098c8e141")
    version("2018.4", sha256="c06425302f2cf668f1bba7a0a03f3c1d34d4ebeef2c72003da308b3947c7f749")
    version("2016.10", sha256="9a43e20aa537cfad8fe7a1715165c91cb4a6935d40947f2d070e4c80f2dcd22b")
    version("2016.6.1", sha256="6f57732f0f8849817e9853eb9d50d85d1ebb1404f702dbc44ee627c642a486ca")
    version("2014.10", sha256="a94138b638907491f473c875e8c95203a6a02efef52b6562be302e435016f4f3")
    version("2014.9", sha256="c5bcbd11cf9847096ae1eb4e83dde75d10ac62efe6e73c4600f3f980968cdbd2")
    version("2015.4", sha256="c4ee70cb407f9284517ac368f121cf0796a7134b961e53d9daf1aaae8f44fb90")
    version("2016.3", sha256="3449da19051655d4c0bb5c37191331748bcad15804d81676a88451ef299370a8")

    depends_on("py-setuptools", type="build")

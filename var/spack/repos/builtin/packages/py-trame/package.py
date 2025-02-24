# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrame(PythonPackage):
    """Trame lets you weave various components and technologies
    into a Web Application solely written in Python."""

    homepage = "http://pythonhosted.org/trame"
    pypi = "trame/trame-3.5.5.tar.gz"

    maintainers("johnwparent")

    license("Apache-2.0", checked_by="johnwparent")

    version("3.5.5", sha256="1e346793d6d38d0ac0695001fea8e3776a4cbb8c890bd70e6e9444db4026ec6b")
    version("3.5.4", sha256="3180d2dec0b3fa96a9ee2a81793cc99e4294dca89a48965e301444af6b8eaaeb")
    version("3.5.3", sha256="b78c9d92016a6f31e66ed8cc4a517f8cf69ad91cd1d6aff4518c76df8840fbed")
    version("3.5.2", sha256="93d97951a4d08fef2ee447e63e8593b6192a30e408637c5b1075fb292e74c8d3")
    version("3.5.1", sha256="10585fb44815da99d038e450208063e3cc7eb38dfbbc2399af7eaa9ead9d17a8")
    version("3.5.0", sha256="706a112bf4164ab8d024301ae0d174bae8df40f2fb82f0ec7b017f53a33bb03f")
    version("3.4.0", sha256="c80e371e89c5b660c223e661569738f4c8c1b1eca2053e049d78ecd009f9756c")
    version("3.3.0", sha256="8359f004b1572dc06937aa903e8a47d6cd6625a5f5ae625db05e6cc7831b724f")
    version("3.2.8", sha256="6f012f8e7cfac215db3405f486d335c670cda5a6b2cdf2539332d523fd201645")
    version("3.2.7", sha256="d222b80f28df620a5a7bd22961601a5900fb490b71d4c0adf71472f836b6e8cb")
    version("3.2.6", sha256="f71c938676b423620cc9036f7df86c1efa2cc2d5e3cf3696fc9b3a1ebba26161")
    version("3.2.5", sha256="03f9afc21154c875fe829965cc7b522e06ecc766347ac0baded611a1f06ba912")
    version("3.2.4", sha256="85b24e4a83cc9cb61854f55db2d5ace8b58468b31f696fa19e576487f62e4152")
    version("3.2.3", sha256="6a1211136600d3523cae73fbc9f02bf0795157d35364adc4aa99cca4b515e812")
    version("3.2.2", sha256="328bf15ad43e07ec747c151d30b230d69e4a32f67a04f346767ae957e8a5047b")
    version("3.2.1", sha256="31a36f4dd7ebba436a0dd868fc1088fc7819f800cfa8bd740965227d0d4d03e3")
    version("3.2.0", sha256="727af2b7297e7a68c6bb0ba2d886c9c340ea8d79038c26790c3f9c218bbfd2b7")
    version("3.1.0", sha256="5f75989f879be5ab69410822c3694219971b42f33551eaa4c023e9a150f2c06b")
    version("3.0.2", sha256="8b3e34bc0216d3089564f0468e451c6d92db5cf209527cb4a4ac13815e6afcb0")
    version("3.0.1", sha256="3a0fcf01d17f7cde1de4cf0b0e775ed7726a1587adee1b23e2908eb49aa3e22d")
    version("3.0.0", sha256="4a1b8988c3eef8523d56132ec641bf8490898e2b50ef379fa0d08ea37554425c")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-trame-client", type=("build", "run"))
    depends_on("py-trame-server", type=("build", "run"))

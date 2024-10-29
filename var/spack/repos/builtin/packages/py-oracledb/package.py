# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOracledb(PythonPackage):
    """Python-oracledb is the new name for the Python cx_Oracle driver.
    The python-oracledb driver is an open source module that enables
    Python programs to access Oracle Database."""

    homepage = "https://oracle.github.io/python-oracledb/"
    pypi = "oracledb/oracledb-1.2.2.tar.gz"

    license("Apache-2.0")

    version("2.4.1", sha256="bd5976bef0e466e0f9d1b9f6531fb5b8171dc8534717ccb04b26e680b6c7571d")
    version("2.4.0", sha256="bdd61a9d5077448b5f1c58af6a14accc287bf8032846c351a3cdde5cf64fe95b")
    version("2.3.0", sha256="b9b0c4ec280b10063e6789bed23ddc2435ae98569ebe64e0b9a270780b9103d5")
    version("2.2.1", sha256="8464c6f0295f3318daf6c2c72c83c2dcbc37e13f8fd44e3e39ff8665f442d6b6")
    version("2.2.0", sha256="f52c7df38b13243b5ce583457b80748a34682b9bb8370da2497868b71976798b")
    version("2.1.2", sha256="3054bcc295d7378834ba7a5aceb865985e954915f9b07a843ea84c3824c6a0b2")
    version("2.1.1", sha256="e2e817cfa6dff36c7131736f34e2aaec75d726fd38d1910d8318061a278228fa")
    version("2.1.0", sha256="1c9a448c9843db33f10b777d6920fb9395eab0b0fdc17f1620fac7c3eecdb57a")
    version("2.0.1", sha256="c12235a9eef123038184e57f3b9b145e149b22654e8242024cf4e81cd890f523")
    version("2.0.0", sha256="fb4481e7ad1a9e81214828a219a45b653301d80c5a1cc47e03857105b61ae2c9")
    version("1.4.2", sha256="e28ed9046f2735dc2dd5bbcdf3667f284e384e0ec7eed3eeb3798fa8a7d47e36")
    version("1.4.1", sha256="bf622581036c7d375664338036fe17effd124ad123c8365e22f2742d0bd237af")
    version("1.4.0", sha256="96ba508f783892c7ca648f268acbcb8a4a9c8037c7dd4a509f05f2c89d6231be")
    version("1.3.2", sha256="bb3c391c167b5778ddb15a7538a2b36db5c9b88a50c86c61781ca9ff302bb643")
    version("1.3.1", sha256="fce1bebdb0d8b88f908e0e1d0d8e5c24ce44e1be041b36032c28c3ba88e21314")
    version("1.3.0", sha256="f105a4705916a28d33e2918fa3634097fe83552bf5ea81afc3a7a68528c9e2f3")
    version("1.2.2", sha256="dd9f63084e44642b484a46b2fcfb4fc921f39facf494a1bab00628fa6409f4fc")
    version("1.2.1", sha256="fb91181294597a1bb56ee273b177d6359e208a63fe0ab61e75ce1368cf02cc9f")
    version("1.2.0", sha256="a69ad4a65872e323a64fd7348eafcc9a1ae7725ddb3918ceb78037f98d6becde")
    version("1.1.1", sha256="88319c122f190b02ddf99cd278c1a7942c361b0037f8d9cf83142b4019c09602")
    version("1.1.0", sha256="a670fd7b48841cceadc90c82c2b61751c6473eba831f2e1ceb97d89e2188e951")
    version("1.0.3", sha256="55bba52d03db740a7f3068167be0a5c027f1931be3ce7cd85d19dda5dfd80e82")
    version("1.0.2", sha256="c5df164aee16ce35c92d6ccbc992a4eabcff304726736defc249e14785acd017")
    version("1.0.1", sha256="9f938134e08a6d08f3886af90a0a9cee197dbe1b38ff7f75f1fc3262d27ba708")
    version("1.0.0", sha256="4a04de68b64789b0a5d80bcd4789c82c4f9a16435dec1b95fff1eee7ad3df6fa")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@40.6.0:", type="build")
    depends_on("py-cryptography@3.2.1:", type=("build", "run"))
    depends_on("py-cython", type="build")
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("oracle-instant-client", type="run", when="impl=thick")

    variant(
        "impl",
        default="thick",
        description="Client Implementation",
        values=("thick", "thin"),
        multi=False,
    )

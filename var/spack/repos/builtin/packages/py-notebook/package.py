# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNotebook(PythonPackage):
    """Jupyter Interactive Notebook"""

    homepage = "https://github.com/jupyter/notebook"
    pypi = "notebook/notebook-6.1.4.tar.gz"

    version("6.5.4", sha256="517209568bd47261e2def27a140e97d49070602eea0d226a696f42a7f16c9a4e")
    version("6.4.12", sha256="6268c9ec9048cff7a45405c990c29ac9ca40b0bc3ec29263d218c5e01f2b4e86")
    version("6.4.11", sha256="709b1856a564fe53054796c80e17a67262071c86bfbdfa6b96aaa346113c555a")
    version("6.4.5", sha256="872e20da9ae518bbcac3e4e0092d5bd35454e847dedb8cb9739e9f3b68406be0")
    version("6.1.4", sha256="687d01f963ea20360c0b904ee7a37c3d8cda553858c8d6e33fd0afd13e89de32")
    version("6.0.3", sha256="47a9092975c9e7965ada00b9a20f0cf637d001db60d241d479f53c0be117ad48")
    version("6.0.1", sha256="660976fe4fe45c7aa55e04bf4bccb9f9566749ff637e9020af3422f9921f9a5d")
    version("6.0.0", sha256="5c16dbf4fa824db19de43637ebfb24bcbd3b4f646e5d6a0414ed3a376d6bc951")
    version("5.7.8", sha256="573e0ae650c5d76b18b6e564ba6d21bf321d00847de1d215b418acb64f056eb8")
    version("5.7.6", sha256="18a98858c0331fb65a60f2ebb6439f8c0c4defd14ca363731b6cabc7f61624b4")
    version("5.7.5", sha256="c5011449a1a6d9f96bf65c4c2d6713802a21125476312b39c99010ccd7a2e2ed")
    version("5.7.4", sha256="d908673a4010787625c8952e91a22adf737db031f2aa0793ad92f6558918a74a")
    version("5.7.3", sha256="f57d470401b2d7434587bcf4dd9263e73f139bf070b1b81a7ed4dfae7ec83f71")
    version("5.7.2", sha256="91705b109fc785198faed892489cddb233265564d5e2dad5e4f7974af05ee8dd")
    version("5.7.1", sha256="24f38c9cc7d7bd0a4c429cc8381e602e58b2b176d6071096a09a0e6c9cd0b463")
    version("5.7.0", sha256="b85e4de3d54cf4f14fe1d0515a980ccb49ddd4cdd21250cc0d4fb6374d50b1a7")
    version("4.2.3", sha256="39a9603d3fe88b60de2903680c965cf643acf2c16fb2c6bac1d905e1042b5851")
    version("4.2.2", sha256="418ba230c9b2e7e739940cae9fb4625e10a63f038e9c95cf1a9b7a244256ba38")
    version("4.2.1", sha256="a49de524dabb99f214bdf2a58f26c7892650251a23a3669c6492fb180492e197")
    version("4.2.0", sha256="e10c4916c77b48394796b5b1440d61d7b210f9941194048fe20ef88948016d84")
    version("4.1.0", sha256="b597437ba33538221008e21fea71cd01eda9da1515ca3963d7c74e44f4b03d90")
    version("4.0.6", sha256="f62e7a6afbc00bab3615b927595d27b1874cff3218bddcbab62f97f6dae567c3")
    version("4.0.4", sha256="a57852514bce1b1cf41fa0311f6cf894960cf68b083b55e6c408316b598d5648")
    version("4.0.2", sha256="8478d7e2ab474855b0ff841f693983388af8662d3af1adcb861acb900274f22a")

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@6.4:")
        depends_on("python@3.6:", when="@6.3:")
        # import pipes in setupbase.py
        depends_on("python@:3.12", when="@:6")

    depends_on("py-jupyter-packaging@0.9:0", when="@6.4.1:", type="build")

    depends_on("py-setuptools", when="@5:", type="build")
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-tornado@6.1:", when="@6.4.5:", type=("build", "run"))
    depends_on("py-tornado@5.0:", when="@6:", type=("build", "run"))
    depends_on("py-tornado@4.1:6", when="@5.7.5:5", type=("build", "run"))
    depends_on("py-tornado@4.0:6", when="@:5.7.4", type=("build", "run"))
    depends_on("py-pyzmq@17:", when="@6:", type=("build", "run"))
    depends_on("py-argon2-cffi", when="@6.1:", type=("build", "run"))
    depends_on("py-traitlets@4.2.1:", when="@5:", type=("build", "run"))
    depends_on("py-traitlets", type=("build", "run"))
    depends_on("py-jupyter-core@4.6.1:", when="@6.0.3:", type=("build", "run"))
    depends_on("py-jupyter-core@4.6.0:", when="@6.0.2", type=("build", "run"))
    depends_on("py-jupyter-core@4.4.0:", when="@5.7.0:6.0.1", type=("build", "run"))
    depends_on("py-jupyter-core", type=("build", "run"))
    depends_on("py-jupyter-client@5.3.4:", when="@6.0.2:", type=("build", "run"))
    depends_on("py-jupyter-client@5.3.1:", when="@6.0.0:6.0.1", type=("build", "run"))
    depends_on("py-jupyter-client@5.2.0:", when="@5.7.0:5", type=("build", "run"))
    depends_on("py-jupyter-client", type=("build", "run"))
    depends_on("py-ipython-genutils", type=("build", "run"))
    depends_on("py-nbformat", type=("build", "run"))
    # https://github.com/jupyter/notebook/pull/6286
    depends_on("py-nbconvert@5:", when="@5.5:", type=("build", "run"))
    depends_on("py-nbconvert", type=("build", "run"))
    depends_on("py-nest-asyncio@1.5:", when="@6.4.10:", type=("build", "run"))
    depends_on("py-ipykernel", type=("build", "run"))
    depends_on("py-send2trash@1.8:", when="@6.4.10:", type=("build", "run"))
    depends_on("py-send2trash@1.5:", when="@6.2.0:", type=("build", "run"))
    depends_on("py-send2trash", when="@6:", type=("build", "run"))
    depends_on("py-terminado@0.8.3:", when="@6.1:", type=("build", "run"))
    depends_on("py-terminado@0.8.1:", when="@5.7.0:", type=("build", "run"))
    depends_on("py-terminado@0.3.3:", when="@:5.7.0", type=("build", "run"))
    depends_on("py-prometheus-client", when="@5.7.0:", type=("build", "run"))
    depends_on("py-nbclassic@0.4.7:", when="@6.5:", type=("build", "run"))

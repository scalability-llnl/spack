# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFastapi(PythonPackage):
    """FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

    homepage = "https://github.com/fastapi/fastapi"
    pypi = "fastapi/fastapi-0.88.0.tar.gz"

    license("MIT")

    version("0.115.4", sha256="db653475586b091cb8b2fec2ac54a680ac6a158e07406e1abae31679e8826349")
    version("0.110.2", sha256="b53d673652da3b65e8cd787ad214ec0fe303cad00d2b529b86ce7db13f17518d")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2024-24762
        version(
            "0.98.0", sha256="0d3c18886f652038262b5898fec6b09f4ca92ee23e9d9b1d1d24e429f84bf27b"
        )
        version(
            "0.88.0", sha256="915bf304180a0e7c5605ec81097b7d4cd8826ff87a02bb198e336fb9f3b5ff02"
        )

    variant("all", default=False, description="Build all optional dependencies")

    depends_on("python@3.8:", when="@0.104:", type=("build", "run"))

    depends_on("py-pdm-backend", when="@0.110.3:", type="build")
    depends_on("py-hatchling@1.13:", when="@0.98:0.110.2", type="build")
    depends_on("py-hatchling", when="@:0.110.2", type="build")

    depends_on("py-starlette@0.40:0.41", when="@0.115.3:", type=("build", "run"))
    depends_on("py-starlette@0.37.2:0.40", when="@0.115.2", type=("build", "run"))
    depends_on("py-starlette@0.37.2:0.38", when="@0.112.1:0.115.1", type=("build", "run"))
    depends_on("py-starlette@0.37.2:0.37", when="@0.110.1:0.112.0", type=("build", "run"))
    depends_on("py-starlette@0.36.3:0.36", when="@0.109.2:0.110.0", type=("build", "run"))
    depends_on("py-starlette@0.35:0.35", when="@0.109.0:0.109.1", type=("build", "run"))
    depends_on("py-starlette@0.29:0.32", when="@0.108.0:0.108", type=("build", "run"))
    depends_on("py-starlette@0.28", when="@0.107.0:0.107", type=("build", "run"))
    depends_on("py-starlette@0.27", when="@0.95.2:0.106", type=("build", "run"))
    depends_on("py-starlette@0.22.0", when="@:0.89.1", type=("build", "run"))
    depends_on("py-pydantic@1.7.4:1,2.1.1:2", when="@0.101:", type=("build", "run"))
    depends_on("py-pydantic@1.7.4:1", when="@0.96.1:", type=("build", "run"))
    depends_on("py-pydantic@1.6.2:1", when="@:0.96.0", type=("build", "run"))
    depends_on("py-typing-extensions@4.8.0:", when="@0.104:", type=("build", "run"))

    conflicts("^py-pydantic@1.7.0:1.7.3,1.8.0:1.8.1,2.0,2.1.0")

    with when("+all"):
        depends_on("py-httpx@0.23:", type=("build", "run"))
        depends_on("py-jinja2@2.11.2:", type=("build", "run"))
        depends_on("py-python-multipart@0.0.7:", when="@0.109.1:", type=("build", "run"))
        depends_on("py-python-multipart@0.0.5:", type=("build", "run"))
        depends_on("py-itsdangerous@1.1:", type=("build", "run"))
        depends_on("py-pyyaml@5.3.1:", type=("build", "run"))
        depends_on("py-ujson@4.0.1:", type=("build", "run"))
        depends_on("py-orjson@3.2.1:", type=("build", "run"))
        depends_on("py-email-validator@2.0.0:", when="@0.100:", type=("build", "run"))
        depends_on("py-email-validator@1.1.1:", type=("build", "run"))
        depends_on("py-uvicorn@0.12:+standard", type=("build", "run"))
        depends_on("py-pydantic-settings@2.0.0:", when="@0.100:", type=("build", "run"))
        depends_on("py-pydantic-extra-types@2.0.0:", when="@0.100:", type=("build", "run"))

        conflicts("^py-ujson@4.0.2,4.1.0,4.2.0,4.3.0,5.0.0,5.1.0")

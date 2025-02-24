# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyWheel(Package, PythonExtension):
    """A built-package format for Python."""

    homepage = "https://github.com/pypa/wheel"
    url = "https://files.pythonhosted.org/packages/py3/w/wheel/wheel-0.41.2-py3-none-any.whl"
    list_url = "https://pypi.org/simple/wheel/"

    version("0.41.2", sha256="75909db2664838d015e3d9139004ee16711748a52c8f336b52882266540215d8")
    version("0.37.1", sha256="4bdcd7d840138086126cd09254dc6195fb4fc6f01c050a1d7236f2630db1d22a")
    version("0.37.0", sha256="21014b2bd93c6d0034b6ba5d35e4eb284340e09d63c59aef6fc14b0f346146fd")
    version("0.36.2", sha256="78b5b185f0e5763c26ca1e324373aadd49182ca90e825f7853f4b2509215dc0e")
    version("0.35.1", sha256="497add53525d16c173c2c1c733b8f655510e909ea78cc0e29d374243544b77a2")
    version("0.34.2", sha256="df277cb51e61359aba502208d680f90c0493adec6f0e848af94948778aed386e")
    version("0.33.6", sha256="f4da1763d3becf2e2cd92a14a7c920f0f00eca30fdde9ea992c836685b9faf28")
    version("0.33.4", sha256="5e79117472686ac0c4aef5bad5172ea73a1c2d1646b808c35926bd26bdfb0c08")
    version("0.33.1", sha256="8eb4a788b3aec8abf5ff68d4165441bc57420c9f64ca5f471f58c3969fe08668")
    version("0.32.3", sha256="1e53cdb3f808d5ccd0df57f964263752aa74ea7359526d3da6c02114ec1e1d44")
    version("0.29.0", sha256="ea8033fc9905804e652f75474d33410a07404c1a78dd3c949a66863bd1050ebd")
    version("0.26.0", sha256="c92ed3a2dd87c54a9e20024fb0a206fe591c352c745fff21e8f8c6cdac2086ea")

    extends("python")
    depends_on("python +ctypes", type=("build", "run"))
    depends_on("python@3.7:", when="@0.38:", type=("build", "run"))
    depends_on("py-pip", type="build")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/w/wheel/wheel-{1}-{0}-none-any.whl"
        if version >= Version("0.38"):
            python = "py3"
        else:
            python = "py2.py3"
        return url.format(python, version)

    def install(self, spec, prefix):
        # To build wheel from source, you need setuptools and wheel already installed.
        # We get around this by using a pre-built wheel, see:
        # https://discuss.python.org/t/bootstrapping-a-specific-version-of-pip/12306
        pip(*PythonPipBuilder.std_args(self), f"--prefix={prefix}", self.stage.archive_file)

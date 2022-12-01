from spack.package import *


class PyLogmuse(PythonPackage):
    """A small logging setup package."""

    homepage = "https://github.com/databio/logmuse/"
    pypi = "logmuse/logmuse-0.2.7.tar.gz"

    version("0.2.7", sha256="a4692c44ddfa912c3cb149ca4c7545f80119aa7485868fd1412e7c647e9a7e7e")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")


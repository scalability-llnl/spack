# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDamask(PythonPackage):
    """Pre- and post-processing tools for DAMASK"""

    homepage = "https://damask-multiphysics.org"
    url = "https://damask-multiphysics.org/download/damask-3.0.0.tar.xz"

    maintainers("MarDiehl")

    license("AGPL-3.0-or-later")

    version("3.0.1", sha256="3db1231f6763356e71b3bb91f66f1abb4fdae2721ce85754fc468446f3d74882")
    version("3.0.0", sha256="aaebc65b3b10e6c313132ee97cfed427c115079b7e438cc0727c5207e159019f")
    version(
        "3.0.0-beta2", sha256="513567b4643f39e27ae32b9f75463fc6f388c1548d42f0393cc87ba02d075f6a"
    )
    version(
        "3.0.0-beta", sha256="1e25e409ac559fc437d1887c6ca930677a732db89a3a32499d545dd75e93925c"
    )
    version(
        "3.0.0-alpha8", sha256="f62c38123213d1c1fe2eb8910b0ffbdc1cac56273c2520f3b64a553363190b9d"
    )
    version(
        "3.0.0-alpha7", sha256="442b06b824441293e72ff91b211a555c5d497aedf62be1c4332c426558b848a4"
    )
    version(
        "3.0.0-alpha6", sha256="de6748c285558dec8f730c4301bfa56b4078c130ff80e3095faf76202f8d2109"
    )
    version(
        "3.0.0-alpha5", sha256="2d2b10901959c26a5bb5c52327cdafc7943bc1b36b77b515b0371221703249ae"
    )
    version(
        "3.0.0-alpha4", sha256="0bb8bde43b27d852b1fb6e359a7157354544557ad83d87987b03f5d629ce5493"
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("py-pandas@0.24:", type=("build", "run"), when="@3.0.0-alpha8:")
    depends_on("py-numpy@1.17:", type=("build", "run"), when="@3.0.0-alpha8:")
    depends_on("py-scipy@1.2:", type=("build", "run"), when="@3.0.0-alpha8:")
    depends_on("py-h5py@2.9:", type=("build", "run"), when="@3.0.0-alpha8:")
    depends_on("vtk+python@8.1:", type=("build", "run"), when="@3.0.0-alpha8:")
    depends_on("py-matplotlib@3.0:", type=("build", "run"), when="@3.0.0-alpha8:")
    depends_on("py-pyyaml@3.12:", type=("build", "run"), when="@3.0.0-alpha8:")
    depends_on("python@3.8:", type=("build", "run"), when="@3.0.0-alpha6:")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@40.6:", type="build")
    depends_on("vtk+python", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))

    patch("setup.patch", when="@3.0.0-alpha7")

    build_directory = "python"

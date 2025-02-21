# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlue(RPackage):
    """Interpreted String Literals.

    An implementation of interpreted string literals, inspired by Python's
    Literal String Interpolation <https://www.python.org/dev/peps/pep-0498/>
    and Docstrings <https://www.python.org/dev/peps/pep-0257/> and Julia's
    Triple-Quoted String Literals <https://docs.julialang.org/en/stable/
    manual/strings/#triple-quoted-string-literals>."""

    cran = "glue"

    license("MIT")

    version("1.7.0", sha256="1af51b51f52c1aeb3bfe9349f55896dd78b5542ffdd5654e432e4d646e4a86dc")
    version("1.6.2", sha256="9da518f12be584c90e75fe8e07f711ee3f6fc0d03d817f72c25dc0f66499fdbf")
    version("1.6.1", sha256="318c2f9544f1204216009f512793c44d6bbe178ff2012f56fa5ffb5e1da978db")
    version("1.6.0", sha256="77bef37ef2c47aad6188ea772880591c5763cce4b1c256e10e68e7c3ec6b4338")
    version("1.4.2", sha256="9f7354132a26e9a876428fa87629b9aaddcd558f9932328e6ac065b95b8ef7ad")
    version("1.4.1", sha256="f8b687d35cacb5ee7fcada6e9c26ea20c04d0bdc9d37e919a03abd1137513bc8")
    version("1.4.0", sha256="ea6c409f7141754baa090deba96cff270a11b185452cf9e6fb69cb148a9069c1")
    version("1.3.1", sha256="4fc1f2899d71a634e1f0adb7942772feb5ac73223891abe30ea9bd91d3633ea8")
    version("1.3.0", sha256="789e5a44c3635c3d3db26666e635e88adcf61cd02b75465125d95d7a12291cee")
    version("1.2.0", sha256="19275b34ee6a1bcad05360b7eb996cebaa1402f189a5dfb084e695d423f2296e")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@1.4.2:")
    depends_on("r@3.4:", type=("build", "run"), when="@1.6.0:")
    depends_on("r@3.6:", when="@1.7.0:", type=("build", "run"))

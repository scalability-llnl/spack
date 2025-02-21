# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCirclize(RPackage):
    """Circular Visualization.

    Circular layout is an efficient way for the visualization of huge amounts
    of information. Here this package provides an implementation  of circular
    layout generation in R as well as an enhancement of available software. The
    flexibility of the package is based on the usage of low-level graphics
    functions such that self-defined high-level graphics can be easily
    implemented by users for specific purposes. Together with the seamless
    connection between the powerful computational and visual environment in R,
    it gives users more convenience and freedom to design figures for  better
    understanding complex patterns behind multiple dimensional data.  The
    package is described in Gu et al. 2014
    <doi:10.1093/bioinformatics/btu393>."""

    cran = "circlize"

    license("MIT")

    version("0.4.16", sha256="16dc32c7704906d13a9e5281bb396e92fb89a6b17fa5e201953240726b650b67")
    version("0.4.15", sha256="d602d55313fe7c675109153d6ed3b99bdba5292e1deefed71d5a21e0db595cc7")
    version("0.4.13", sha256="6cbadbf8e8b1abbd71a79080677d2b95f2bdd18f2e4d707c32d5c2ff26c5369b")
    version("0.4.12", sha256="b3b60caa5292cf980cf474c85f59582f6862925631a4da86a78eac05903252f4")
    version("0.4.6", sha256="cec88cfc5e512a111cc37177552c25698ccc0e9bbecb0d6e60657e7b115a56fa")
    version("0.4.1", sha256="204a170ae3b982f09b652c4583189907cfa42a29bc7efaba02a1e0d79f1cf1f0")
    version("0.4.0", sha256="abdc1bbe264be42c1d7b65869979da7cd131032fd6fd3f11f9744dae54e83f5c")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.4.16:")
    depends_on("r-globaloptions@0.1.0:", type=("build", "run"))
    depends_on("r-globaloptions@0.1.2:", type=("build", "run"), when="@0.4.12:")
    depends_on("r-shape", type=("build", "run"))
    depends_on("r-colorspace", type=("build", "run"))

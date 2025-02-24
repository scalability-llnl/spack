# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGwmodel(RPackage):
    """Geographically-Weighted Models.

    Techniques from a particular branch of spatial statistics,termed
    geographically-weighted (GW) models. GW models suit situations when data
    are not described well by some global model, but where there are spatial
    regions where a suitably localised calibration provides a better
    description. 'GWmodel' includes functions to calibrate: GW summary
    statistics (Brunsdon et al., 2002) <doi:10.1016/s0198-9715(01)00009-6>, GW
    principal components analysis (Harris et al., 2011)
    <doi:10.1080/13658816.2011.554838>, GW discriminant analysis (Brunsdon et
    al., 2007) <doi:10.1111/j.1538-4632.2007.00709.x> and various forms of GW
    regression (Brunsdon et al., 1996)
    <doi:10.1111/j.1538-4632.1996.tb00936.x>; some of which are provided in
    basic and robust (outlier resistant) forms."""

    cran = "GWmodel"

    version("2.3-3", sha256="5f69d000d7ffba491f1dafbad5ec0b5fcbbdb28831092252a8b409163d6ad33c")
    version("2.2-9", sha256="3696e0f24994df4f393dbcb2e74bc0808704b80e1203247be3911fc3bcdb5f18")
    version("2.2-8", sha256="5b1890dbf75502e89b651efd9158be77b3cfa764a5717f9889f438ed2b0a4da2")
    version("2.2-2", sha256="4e2b221b85fbc828ffc4f057c137ded849afcaac2a75c27d2d6d0a6db17f8a06")
    version("2.1-3", sha256="3e1a36fddf8e64f61d548067bb043216f8d12069d814a4cbf07a9cae0b310af6")
    version("2.1-1", sha256="91241b4e26d423a54c7c6784ef5159759058a5dafdff18a1ea8451faf979d1f3")
    version("2.0-9", sha256="b479af2c19d4aec30f1883d00193d52e342c609c1badcb51cc0344e4404cffa7")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-robustbase", type=("build", "run"))
    depends_on("r-sf", type=("build", "run"), when="@2.3-1:")
    depends_on("r-sp", type=("build", "run"))
    depends_on("r-sp@1.4-0.1:", type=("build", "run"), when="@2.2-0:")
    depends_on("r-spatialreg", type=("build", "run"))
    depends_on("r-spacetime", type=("build", "run"))
    depends_on("r-spdep", type=("build", "run"))
    depends_on("r-fnn", type=("build", "run"), when="@2.1-1:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcpp@1.0.12:", type=("build", "run"), when="@2.3-3:")
    depends_on("r-rcpparmadillo", type=("build", "run"))
    depends_on("r-rcppeigen", type=("build", "run"), when="@2.3-3:")
    depends_on("gmake", type="build")

    depends_on("r-maptools@0.5-2:", type=("build", "run"), when="@:2.2")

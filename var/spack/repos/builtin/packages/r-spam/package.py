# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpam(RPackage):
    """SPArse Matrix.

    Set of functions for sparse matrix algebra. Differences with other sparse
    matrix packages are: (1) we only support (essentially) one sparse matrix
    format, (2) based on transparent and simple structure(s), (3) tailored for
    MCMC calculations within G(M)RF. (4) and it is fast and scalable (with the
    extension package spam64). Documentation about 'spam' is provided by
    vignettes included in this package, see also Furrer and Sain (2010)
    <doi:10.18637/jss.v036.i10>; see 'citation("spam")' for details."""

    cran = "spam"

    license("LGPL-2.0-only OR BSD-3-Clause")

    version("2.10-0", sha256="719c86a23801ecf051ffd8291912ee3567af4010e74af470fbf09e274728ac79")
    version("2.9-1", sha256="c32e219279988b1bfc258aaf64f5a46efa558202848a9ae64946ffbe8b497ddb")
    version("2.8-0", sha256="d98177435b028d1c706d0197ea8132bfaffae6052c3ce6064a7f64178512d6aa")
    version("2.6-0", sha256="638fdd658e94f7544b46f6b6568b20a9f390bcd703aff572a3a5249fef66be5c")
    version("2.3-0.2", sha256="848fa95c0a71ac82af6344539af7b1c33563c687f06ead42851a68b621fff533")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@2.9-1:")
    depends_on("r-dotcall64", type=("build", "run"))
    depends_on("r-rcpp@1.0.8.3:", type=("build", "run"), when="@2.10-0:")

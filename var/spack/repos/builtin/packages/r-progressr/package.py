# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProgressr(RPackage):
    """An Inclusive, Unifying API for Progress Updates.

    A minimal, unifying API for scripts and packages to report progress updates
    from anywhere including when using parallel processing. The package is
    designed such that the developer can to focus on what progress should be
    reported on without having to worry about how to present it. The end user
    has full control of how, where, and when to render these progress updates,
    e.g. in the terminal using utils::txtProgressBar() or
    progress::progress_bar(), in a graphical user interface using
    utils::winProgressBar(), tcltk::tkProgressBar() or shiny::withProgress(),
    via the speakers using beep::beepr(), or on a file system via the size of a
    file. Anyone can add additional, customized, progression handlers. The
    'progressr' package uses R's condition framework for signaling progress
    updated. Because of this, progress can be reported from almost anywhere in
    R, e.g. from classical for and while loops, from map-reduce API:s like the
    lapply() family of functions, 'purrr', 'plyr', and 'foreach'. It will also
    work with parallel processing via the 'future' framework, e.g.
    future.apply::future_lapply(), furrr::future_map(), and 'foreach' with
    'doFuture'. The package is compatible with Shiny applications."""

    cran = "progressr"

    license("GPL-3.0-or-later")

    version("0.14.0", sha256="9a2899f879a5577f043be99c18d52bfe4d655cc52a96cae834e8a301b36258af")
    version("0.13.0", sha256="0ffb3dcadde0cc191bad0ff9e05d000aa65e2fc339cfc94ebbb263088df5a4e1")
    version("0.11.0", sha256="d8668c82348a20cca34bb18c0c94e6083dbb6dbea40615e07e4161aff7366cd9")
    version("0.10.1", sha256="8f83024b2a6f52996750d45bf6698c2b438fb1062985f1df936ba3af313caed1")
    version("0.10.0", sha256="4c95dc11c50c792440fa17f4538d59f1f3012bf6ef462a5a141609f87319badc")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))

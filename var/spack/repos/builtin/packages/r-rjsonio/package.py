# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRjsonio(RPackage):
    """Serialize R Objects to JSON, JavaScript Object Notation.

    This is a package that allows conversion to and from data in Javascript
    object notation (JSON) format. This allows R objects to be inserted into
    Javascript/ECMAScript/ActionScript code and allows R programmers to read
    and convert JSON content to R objects. This is an alternative to rjson
    package. Originally, that was too slow for converting large R objects to
    JSON and was not extensible. rjson's performance is now similar to this
    package, and perhaps slightly faster in some cases. This package uses
    methods and is readily extensible by defining methods for different
    classes, vectorized operations, and C code and callbacks to R functions for
    deserializing JSON objects to R. The two packages intentionally share the
    same basic interface. This package (RJSONIO) has many additional options to
    allow customizing the generation and processing of JSON content. This
    package uses libjson rather than implementing yet another JSON parser. The
    aim is to support other general projects by building on their work,
    providing feedback and benefit from their ongoing development."""

    cran = "RJSONIO"

    version("1.3-1.9", sha256="f173034b0c28873f417ee804b9e278aedd92e76eb56c7c6d71b1c02fa1193ece")
    version("1.3-1.8", sha256="f6f0576d3c7852b16295dfc897feebca064fe5dd29cdce7592f94c56823553f5")
    version("1.3-1.6", sha256="82d1c9ea7758b2a64ad683f9c46223dcba9aa8146b43c1115bf9aa76a657a09f")
    version("1.3-1.4", sha256="54142c931e15eca278a02dad5734026bb49d960471eb085008af825352953190")
    version("1.3-1.2", sha256="550e18f7c04186376d67747b8258f529d205bfc929da9194fe45ec384e092d7e")
    version("1.3-1.1", sha256="c72493b441758cd1e3e9d91296b9ea31068e71104649f46ad84c854a02c09693")
    version("1.3-0", sha256="119334b7761c6c1c3cec52fa17dbc1b72eaebb520c53e68d873dea147cf48fb7")

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProcessx(RPackage):
    """Execute and Control System Processes.

    Tools to run system processes in the background. It can check if a
    background process is running; wait on a background process to finish; get
    the exit status of finished processes; kill background processes. It can
    read the standard output and error of the processes, using non-blocking
    connections. 'processx' can poll a process for standard output or error,
    with a timeout. It can also poll several processes at once."""

    cran = "processx"

    license("MIT")

    version("3.8.4", sha256="6627672d7fb109f37dc1d0eaef913f4cfc7ad8ac807abf0397e6d37753b1e70b")
    version("3.8.1", sha256="e008472b81d4ca1a37a4ba7dd58e5e944f96ab2e44c8ccc8840d43e9fe99e93c")
    version("3.8.0", sha256="9270d9d26c4314151062801a5c1fc57556b4fcb41dbf3558cb5bd230b18ffb0b")
    version("3.7.0", sha256="de6a8d4135fc53ec35043fbaf6b000dc9597719345595d8479662a39dad55ed3")
    version("3.5.3", sha256="679629fa56ec185d4fd52ade5b699c78a2a0e875acdf57555b31bc62111f342a")
    version("3.5.2", sha256="ed6f2d1047461c6061e6ed58fb6de65a289b56009867892abad76c6bba46fc2b")
    version("3.4.5", sha256="e368103aa6a6894bfa8e78b12a25598464bcd2c19a8b6334f24ee397db13bb14")
    version("3.4.1", sha256="f1abddb48fa78f2b176552e2ec5d808d4d87d79ce72e9b3d25c9a7d715bbd1bc")
    version("3.3.1", sha256="6123dbdf9f3bb6e5e8678980fb4587dcefb56d2190adf2ef494d7cd199720bae")
    version("3.2.0", sha256="c4ba602fcbdc032ae9d94701b3e6b83a2dab1b53d0b4f9937b07a84eae22fddf")
    version("3.1.0", sha256="11ac120ab4e4aa0e99c9b2eda87d07bc683bab735f1761e95e5ddacd311b5972")
    version("3.0.3", sha256="53781dba3c538605a02e28b3b577e7de79e2064bfc502025f7ec0e5945e302bf")
    version("2.0.0.1", sha256="8f61b2952d0f2d13c74465bfba174ce11eee559475c2f7b9be6bcb9e2e1d827b")
    version("2.0.0", sha256="8325b56a60a276909228756281523cda9256bc754c5f3ca03b41c5c17cc398ad")

    depends_on("r@3.4.0:", type=("build", "run"), when="@3.5.3:")
    depends_on("r-ps@1.2.0:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-r6", type=("build", "run"))

    depends_on("r-assertthat", type=("build", "run"), when="@:3.2.9")
    depends_on("r-crayon", type=("build", "run"), when="@:3.2.9")
    depends_on("r-debugme", type=("build", "run"), when="@:3.0.9")

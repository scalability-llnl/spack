# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Astra(Package):
    """A Space Charge Tracking Algorithm."""

    homepage = "https://www.desy.de/~mpyflo/"

    version(
        "2020-02-03",
        sha256="ca9ee7d3d369f9040fbd595f57f3153f712d789b66385fd2d2de88a69a774b83",
        expand=False,
        url="https://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/Astra",
    )

    # no longer available?
    # version('2016-11-30',
    #         sha256='50738bf924724e2dd15f1d924b290ffb0f7c703e5d5ae02ffee2db554338801e',
    #         expand=False,
    #         url='https://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/Astra')

    variant("gui", default=False, description="Install plotting/gui tools")

    resource(
        name="generator",
        url="https://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/generator",
        sha256="d31cf9fcfeb90ce0e729d8af628caf4a23f7e588a3d412d5b19241e8c684e531",
        expand=False,
        placement="generator",
    )
    resource(
        name="postpro",
        url="https://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/postpro",
        sha256="f47efb14748ce1da62bcd33c9411482bee89bcab75b28a678fc764db0c21ee8d",
        expand=False,
        when="+gui",
        placement="postpro",
    )
    resource(
        name="fieldplot",
        url="https://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/fieldplot",
        sha256="89df1da96bfd9f165fa148b84376af558e6633ab2dda837273706143ff863c96",
        expand=False,
        when="+gui",
        placement="fieldplot",
    )
    resource(
        name="lineplot",
        url="https://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/lineplot",
        sha256="d2d5702be9cb3d96391c6a0ca37366d580ced1f0f722fb33a6039ad7fd43b69a",
        expand=False,
        when="+gui",
        placement="lineplot",
    )
    resource(
        name="pgxwin_server",
        url="https://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/pgxwin_server",
        sha256="d2d5702be9cb3d96391c6a0ca37366d580ced1f0f722fb33a6039ad7fd43b69a",
        expand=False,
        when="+gui",
        placement="pgxwin_server",
    )

    depends_on("libxcb", when="+gui")
    depends_on("libx11", when="+gui")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("Astra", prefix.bin)
        install("generator/generator", prefix.bin)
        if spec.satisfies("+gui"):
            install("postpro/postpro", prefix.bin)
            install("fieldplot/fieldplot", prefix.bin)
            install("lineplot/lineplot", prefix.bin)
            install("pgxwin_server/pgxwin_server", prefix.bin)

        chmod = which("chmod")
        chmod("+x", join_path(prefix.bin, "Astra"))
        chmod("+x", join_path(prefix.bin, "generator"))
        if spec.satisfies("+gui"):
            chmod("+x", join_path(prefix.bin, "postpro"))
            chmod("+x", join_path(prefix.bin, "fieldplot"))
            chmod("+x", join_path(prefix.bin, "lineplot"))
            chmod("+x", join_path(prefix.bin, "pgxwin_server"))

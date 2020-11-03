# Copyright 2019-2020 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
archspec command line interface
"""

import click

import archspec
import archspec.cpu


@click.group(name="archspec")
@click.version_option(version=archspec.__version__)
def main():
    """archspec command line interface"""


@main.command()
def cpu():
    """archspec command line interface for CPU"""
    click.echo(archspec.cpu.host())

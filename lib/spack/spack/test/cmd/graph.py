# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand, SpackCommandError

graph = SpackCommand("graph")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_ascii():
    """Tests spack graph --ascii"""
    graph("--ascii", "dt-diamond")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_dot():
    """Tests spack graph --dot"""
    graph("--dot", "dt-diamond")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_static():
    """Tests spack graph --static"""
    graph("--static", "dt-diamond")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_installed():
    """Tests spack graph --installed"""

    graph("--installed")

    with pytest.raises(SpackCommandError):
        graph("--installed", "dt-diamond")


@pytest.mark.db
@pytest.mark.usefixtures("mock_packages", "database")
def test_graph_deptype():
    """Tests spack graph --deptype"""
    graph("--deptype", "all", "dt-diamond")


def test_graph_no_specs():
    """Tests spack graph with no arguments"""

    with pytest.raises(SpackCommandError):
        graph()

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.main import SpackCommand

spack_test = SpackCommand("unit-test")
cmd_test_py = os.path.join("lib", "spack", "spack", "test", "cmd", "unit_test.py")


def test_list():
    output = spack_test("--list")
    assert "unit_test.py" in output
    assert "spec_semantics.py" in output
    assert "test_list" not in output


def test_list_with_pytest_arg():
    output = spack_test("--list", cmd_test_py)
    assert output.strip() == cmd_test_py


def test_list_with_keywords():
    # Here we removed querying with a "/" to separate directories
    # since the behavior is inconsistent across different pytest
    # versions, see https://stackoverflow.com/a/48814787/771663
    output = spack_test("--list", "-k", "unit_test.py")
    assert output.strip() == cmd_test_py


def test_list_long(capsys):
    with capsys.disabled():
        output = spack_test("--list-long")
    assert "unit_test.py::\n" in output
    assert "test_list" in output
    assert "test_list_with_pytest_arg" in output
    assert "test_list_with_keywords" in output
    assert "test_list_long" in output
    assert "test_list_long_with_pytest_arg" in output
    assert "test_list_names" in output
    assert "test_list_names_with_pytest_arg" in output

    assert "spec_dag.py::\n" in output
    assert "test_installed_deps" in output
    assert "test_test_deptype" in output


def test_list_long_with_pytest_arg(capsys):
    with capsys.disabled():
        output = spack_test("--list-long", cmd_test_py)
    print(output)
    assert "unit_test.py::\n" in output
    assert "test_list" in output
    assert "test_list_with_pytest_arg" in output
    assert "test_list_with_keywords" in output
    assert "test_list_long" in output
    assert "test_list_long_with_pytest_arg" in output
    assert "test_list_names" in output
    assert "test_list_names_with_pytest_arg" in output

    assert "spec_dag.py::\n" not in output
    assert "test_installed_deps" not in output
    assert "test_test_deptype" not in output


def test_list_names():
    output = spack_test("--list-names")
    assert "unit_test.py::test_list\n" in output
    assert "unit_test.py::test_list_with_pytest_arg\n" in output
    assert "unit_test.py::test_list_with_keywords\n" in output
    assert "unit_test.py::test_list_long\n" in output
    assert "unit_test.py::test_list_long_with_pytest_arg\n" in output
    assert "unit_test.py::test_list_names\n" in output
    assert "unit_test.py::test_list_names_with_pytest_arg\n" in output

    assert "spec_dag.py::test_installed_deps\n" in output
    assert "spec_dag.py::test_test_deptype\n" in output


def test_list_names_with_pytest_arg():
    output = spack_test("--list-names", cmd_test_py)
    assert "unit_test.py::test_list\n" in output
    assert "unit_test.py::test_list_with_pytest_arg\n" in output
    assert "unit_test.py::test_list_with_keywords\n" in output
    assert "unit_test.py::test_list_long\n" in output
    assert "unit_test.py::test_list_long_with_pytest_arg\n" in output
    assert "unit_test.py::test_list_names\n" in output
    assert "unit_test.py::test_list_names_with_pytest_arg\n" in output

    assert "spec_dag.py::test_installed_deps\n" not in output
    assert "spec_dag.py::test_test_deptype\n" not in output


def test_pytest_help():
    output = spack_test("--pytest-help")
    assert "-k EXPRESSION" in output
    assert "pytest-warnings:" in output
    assert "--collect-only" in output

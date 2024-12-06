# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for provider index cache files.

Tests assume that mock packages provide this::

  {'blas':   {
       blas: set([netlib-blas, openblas, openblas-with-lapack])},
   'lapack': {lapack: set([netlib-lapack, openblas-with-lapack])},
   'mpi': {mpi@:1: set([mpich@:1]),
                    mpi@:2.0: set([mpich2]),
                    mpi@:2.1: set([mpich2@1.1:]),
                    mpi@:2.2: set([mpich2@1.2:]),
                    mpi@:3: set([mpich@3:]),
                    mpi@:10.0: set([zmpi])},
    'stuff': {stuff: set([externalvirtual])}}
"""
import io

import spack.repo
from spack.provider_index import ProviderIndex
from spack.spec import Spec


def test_provider_index_round_trip(mock_packages):
    p = ProviderIndex(specs=spack.repo.all_package_names(), repository=spack.repo.PATH)

    ostream = io.StringIO()
    p.to_json(ostream)

    istream = io.StringIO(ostream.getvalue())
    q = ProviderIndex.from_json(istream, repository=spack.repo.PATH)

    assert p == q


def test_providers_for_simple(mock_packages):
    p = ProviderIndex(specs=spack.repo.all_package_names(), repository=spack.repo.PATH)

    blas_providers = p.providers_for("blas")
    assert Spec("netlib-blas") in blas_providers
    assert Spec("openblas") in blas_providers
    assert Spec("openblas-with-lapack") in blas_providers

    lapack_providers = p.providers_for("lapack")
    assert Spec("netlib-lapack") in lapack_providers
    assert Spec("openblas-with-lapack") in lapack_providers


def test_mpi_providers(mock_packages):
    p = ProviderIndex(specs=spack.repo.all_package_names(), repository=spack.repo.PATH)

    mpi_2_providers = p.providers_for("mpi@2")
    assert Spec("mpich2") in mpi_2_providers
    assert Spec("mpich@3:") in mpi_2_providers

    mpi_3_providers = p.providers_for("mpi@3")
    assert Spec("mpich2") not in mpi_3_providers
    assert Spec("mpich@3:") in mpi_3_providers
    assert Spec("zmpi") in mpi_3_providers


def test_equal(mock_packages):
    p = ProviderIndex(specs=spack.repo.all_package_names(), repository=spack.repo.PATH)
    q = ProviderIndex(specs=spack.repo.all_package_names(), repository=spack.repo.PATH)
    assert p == q


def test_copy(mock_packages):
    p = ProviderIndex(specs=spack.repo.all_package_names(), repository=spack.repo.PATH)
    q = p.copy()
    assert p == q

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib

import pytest

import spack.concretize
import spack.modules.lmod
import spack.modules.tcl
import spack.spec


@pytest.fixture()
def modulefile_content(request):
    """Returns a function that generates the content of a module file as a list of lines."""
    writer_cls = getattr(request.module, "writer_cls")

    def _impl(spec_like, module_set_name="default", explicit=True):
        if isinstance(spec_like, str):
            spec_like = spack.spec.Spec(spec_like)
        spec = spack.concretize.concretize_one(spec_like)
        generator = writer_cls(spec, module_set_name, explicit)
        generator.write(overwrite=True)
        written_module = pathlib.Path(generator.layout.filename)
        content = written_module.read_text(encoding="utf-8").splitlines()
        generator.remove()
        return content

    return _impl


@pytest.fixture()
def factory(request, mock_modules_root):
    """Given a spec string, returns an instance of the writer and the corresponding spec."""
    writer_cls = getattr(request.module, "writer_cls")

    def _mock(spec_string, module_set_name="default", explicit=True):
        spec = spack.concretize.concretize_one(spec_string)
        return writer_cls(spec, module_set_name, explicit), spec

    return _mock


@pytest.fixture()
def mock_module_filename(monkeypatch, tmp_path):
    filename = tmp_path / "module"
    # Set for both module types so we can test both
    monkeypatch.setattr(spack.modules.lmod.LmodFileLayout, "filename", str(filename))
    monkeypatch.setattr(spack.modules.tcl.TclFileLayout, "filename", str(filename))
    yield str(filename)

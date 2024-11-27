.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. extensions:

=================
Custom Extensions
=================

*Spack extensions* allow you to extend Spack capabilities by deploying your
own custom commands or logic in an arbitrary location on your filesystem.
This might be extremely useful e.g. to develop and maintain a command whose purpose is
too specific to be considered for reintegration into the mainline or to
evolve a command through its early stages before starting a discussion to merge
it upstream.

From Spack's point of view an extension is any path in your filesystem which
respects the following naming and layout for files:

.. code-block:: console

  spack-scripting/ # The top level directory must match the format 'spack-{extension_name}'
  ├── pytest.ini # Optional file if the extension ships its own tests
  ├── scripting # Folder that may contain modules that are needed for the extension commands
  │   ├── cmd # Folder containing extension commands
  │   │   └── filter.py # A new command that will be available
  │   └── functions.py # Module with internal details
  └── tests # Tests for this extension
  │   ├── conftest.py
  │   └── test_filter.py
  └── templates # Templates that may be needed by the extension

In the example above, the extension is named *scripting*. It adds an additional command
(``spack filter``) and unit tests to verify its behavior.

The extension can import any core Spack module in its implementation. When loaded by
the ``spack`` command, the extension itself is imported as a Python package in the
``spack.extensions`` namespace. In the example above, since the extension is named
"scripting", the corresponding Python module is ``spack.extensions.scripting``.

The code for this example extension can be obtained by cloning the corresponding git repository:

.. code-block:: console

   $ git -C /tmp clone https://github.com/spack/spack-scripting.git

---------------------------------
Configure Spack to Use Extensions
---------------------------------

To make your current Spack instance aware of extensions you should add their root
paths to ``config.yaml``. In the case of our example this means ensuring that:

.. code-block:: yaml

   config:
     extensions:
     - /tmp/spack-scripting

is part of your configuration file. Once this is setup any command that the extension provides
will be available from the command line:

.. code-block:: console

   $ spack filter --help
   usage: spack filter [-h] [--installed | --not-installed]
                       [--explicit | --implicit] [--output OUTPUT]
                       ...

   filter specs based on their properties

   positional arguments:
     specs            specs to be filtered

   optional arguments:
     -h, --help       show this help message and exit
     --installed      select installed specs
     --not-installed  select specs that are not yet installed
     --explicit       select specs that were installed explicitly
     --implicit       select specs that are not installed or were installed implicitly
     --output OUTPUT  where to dump the result

The corresponding unit tests can be run giving the appropriate options to ``spack unit-test``:

.. code-block:: console

   $ spack unit-test --extension=scripting
   ========================================== test session starts ===========================================
   platform linux -- Python 3.11.5, pytest-7.4.3, pluggy-1.3.0
   rootdir: /home/culpo/github/spack-scripting
   configfile: pytest.ini
   testpaths: tests
   plugins: xdist-3.5.0
   collected 5 items

   tests/test_filter.py .....                                                                         [100%]

   ========================================== slowest 30 durations ==========================================
   2.31s setup    tests/test_filter.py::test_filtering_specs[kwargs0-specs0-expected0]
   0.57s call     tests/test_filter.py::test_filtering_specs[kwargs2-specs2-expected2]
   0.56s call     tests/test_filter.py::test_filtering_specs[kwargs4-specs4-expected4]
   0.54s call     tests/test_filter.py::test_filtering_specs[kwargs3-specs3-expected3]
   0.54s call     tests/test_filter.py::test_filtering_specs[kwargs1-specs1-expected1]
   0.48s call     tests/test_filter.py::test_filtering_specs[kwargs0-specs0-expected0]
   0.01s setup    tests/test_filter.py::test_filtering_specs[kwargs4-specs4-expected4]
   0.01s setup    tests/test_filter.py::test_filtering_specs[kwargs2-specs2-expected2]
   0.01s setup    tests/test_filter.py::test_filtering_specs[kwargs1-specs1-expected1]
   0.01s setup    tests/test_filter.py::test_filtering_specs[kwargs3-specs3-expected3]

   (5 durations < 0.005s hidden.  Use -vv to show these durations.)
   =========================================== 5 passed in 5.06s ============================================

---------------------------------------
Registering Extensions via Entry Points
---------------------------------------

.. note::
   Python version >= 3.8 is required to register extensions via entry points.

Spack can be made aware of extensions that are installed as part of a python package.  To do so, register a function that returns the extension path, or paths, to the ``"spack.extensions"`` entry point.  Consider the Python package ``my_package`` that includes a Spack extension:

.. code-block:: console

  my-package/
  ├── src
  │   ├── my_package
  │   │   └── __init__.py
  │   └── spack-scripting/  # the spack extensions
  └── pyproject.toml

adding the following to ``my_package``'s ``pyproject.toml`` will make the ``spack-scripting`` extension visible to Spack when ``my_package`` is installed:

.. code-block:: toml

   [project.entry_points."spack.extenions"]
   my_package = "my_package:get_extension_path"

The function ``my_package.get_extension_path`` in ``my_package/__init__.py`` might look like

.. code-block:: python

   import importlib.resources

   def get_extension_path():
       dirname = importlib.resources.files("my_package").joinpath("spack-scripting")
       if dirname.exists():
           return str(dirname)

.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. extensions:

=================
Custom Extensions
=================

*Spack extensions* permit you to extend Spack capabilities by deploying your
own custom commands or logic in an arbitrary location on your filesystem.
This might be extremely useful e.g. to develop and maintain a command whose purpose is
too specific to be considered for reintegration into the mainline or to
evolve a command through its early stages before starting a discussion to merge
it upstream.
From Spack's point of view an extension is any path in your filesystem which
respects a prescribed naming and layout for files:

.. code-block:: console

  spack-scripting/ # The top level directory must match the format 'spack-{extension_name}'
  ├── pytest.ini # Optional file if the extension ships its own tests
  ├── scripting # Folder that may contain modules that are needed for the extension commands
  │   └── cmd # Folder containing extension commands
  │       └── filter.py # A new command that will be available
  ├── tests # Tests for this extension
  │   ├── conftest.py
  │   └── test_filter.py
  └── templates # Templates that may be needed by the extension

In the example above the extension named *scripting* adds an additional command (``filter``)
and unit tests to verify its behavior. The code for this example can be
obtained by cloning the corresponding git repository:

.. TODO: write an ad-hoc "hello world" extension and make it part of the spack organization

.. code-block:: console

   $ cd ~/
   $ mkdir tmp && cd tmp
   $ git clone https://github.com/alalazo/spack-scripting.git
   Cloning into 'spack-scripting'...
   remote: Counting objects: 11, done.
   remote: Compressing objects: 100% (7/7), done.
   remote: Total 11 (delta 0), reused 11 (delta 0), pack-reused 0
   Receiving objects: 100% (11/11), done.

As you can see by inspecting the sources, Python modules that are part of the extension
can import any core Spack module.

---------------------------------
Configure Spack to Use Extensions
---------------------------------

To make your current Spack instance aware of extensions you should add their root
paths to ``config.yaml``. In the case of our example this means ensuring that:

.. code-block:: yaml

   config:
     extensions:
     - ~/tmp/spack-scripting

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

The corresponding unit tests can be run giving the appropriate options
to ``spack unit-test``:

.. code-block:: console

   $ spack unit-test --extension=scripting

   ============================================================== test session starts ===============================================================
   platform linux2 -- Python 2.7.15rc1, pytest-3.2.5, py-1.4.34, pluggy-0.4.0
   rootdir: /home/mculpo/tmp/spack-scripting, inifile: pytest.ini
   collected 5 items

   tests/test_filter.py ...XX
   ============================================================ short test summary info =============================================================
   XPASS tests/test_filter.py::test_filtering_specs[flags3-specs3-expected3]
   XPASS tests/test_filter.py::test_filtering_specs[flags4-specs4-expected4]

   =========================================================== slowest 20 test durations ============================================================
   3.74s setup    tests/test_filter.py::test_filtering_specs[flags0-specs0-expected0]
   0.17s call     tests/test_filter.py::test_filtering_specs[flags3-specs3-expected3]
   0.16s call     tests/test_filter.py::test_filtering_specs[flags2-specs2-expected2]
   0.15s call     tests/test_filter.py::test_filtering_specs[flags1-specs1-expected1]
   0.13s call     tests/test_filter.py::test_filtering_specs[flags4-specs4-expected4]
   0.08s call     tests/test_filter.py::test_filtering_specs[flags0-specs0-expected0]
   0.04s teardown tests/test_filter.py::test_filtering_specs[flags4-specs4-expected4]
   0.00s setup    tests/test_filter.py::test_filtering_specs[flags4-specs4-expected4]
   0.00s setup    tests/test_filter.py::test_filtering_specs[flags3-specs3-expected3]
   0.00s setup    tests/test_filter.py::test_filtering_specs[flags1-specs1-expected1]
   0.00s setup    tests/test_filter.py::test_filtering_specs[flags2-specs2-expected2]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags2-specs2-expected2]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags1-specs1-expected1]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags0-specs0-expected0]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags3-specs3-expected3]
   ====================================================== 3 passed, 2 xpassed in 4.51 seconds =======================================================

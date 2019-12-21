.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

In the example above the extension named ``spack-scripting`` adds an additional ``filter``
command and unit tests to verify its behavior. Spack provides a convenient command
line interface to work with extensions. All its functionalities are grouped within
a single command:

.. code-block:: console

   $ spack command-extensions -h
   usage: spack command-extensions [-h] SUBCOMMAND ...

   manage custom extensions to Spack

   positional arguments:
     SUBCOMMAND
       get       gets a custom extension from a URL
       remove    removes a currently installed extension
       update    ensure a custom extension is up to date
       list      list all available custom extensions
       inspect   returns information on a given extension

   optional arguments:
     -h, --help  show this help message and exit

-------------------------------
Install and remove an extension
-------------------------------

To install the ``spack-scripting`` extension shown in the previous section
all you need to do is specify its Github path on the command line:

.. code-block:: console

   $ spack command-extensions get github.com/alalazo/spack-scripting
   ==> Cloning custom extension from : https://github.com/alalazo/spack-scripting.git@master
   ==> Extension "spack-scripting" has been installed and it is ready to be used

Currently the command line manages only extensions hosted on Github, but the
number of supported hosts will be extended in the future. You can then check
the list of installed extensions:

.. code-block:: console

   $ spack command-extensions list
   ---- "user/linux" scope ----
       spack-scripting

and make sure ``spack-scripting`` appears there. As you might have noticed the
configuration scope where the extension was installed is reported. Like many
other features in Spack, also command extensions are configuration driven and
the command line interface is just a convenient way to manage the corresponding
YAML file:

.. code-block:: yaml

   config:
     extensions:
     - name: spack-scripting
       version:
         type: branch
         value: master
       root: /home/user/.spack/extensions
       url: github.com/alalazo/spack-scripting

To remove an installed extension you just need to use the corresponding subcommand:

.. code-block:: console

   $ spack command-extensions remove spack-scripting
   ==> Extension "spack-scripting" removed from "user/linux" scope

   $ spack command-extensions list
   ==> No extensions found

By default removing an extension does not delete the repository that was checked out, so
that it can be reused if you add it back later. If you want to prune the repository though
there is an option:

.. code-block:: console

   $ spack command-extensions remove --delete spack-scripting

-----------------------
Inspecting an extension
-----------------------

Once an extension is installed, it is possible to inspect it:

.. code-block:: console

   $ spack command-extensions inspect spack-scripting
   NAME:             spack-scripting
   VERSION:          master
   LOCAL REPOSITORY: /home/user/.spack/extensions/spack-scripting
   COMMANDS:         filter

and get more information on the commands it provides or the location of the local repository.
In this case the extension provides the additional ``filter`` command.
Let's verify it is available from the command line:

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

The corresponding unit tests can be run giving the appropriate options to ``spack test``:

.. code-block:: console

   $ spack test --extension=spack-scripting
   =================================================================== test session starts ====================================================================
   platform linux -- Python 3.7.4, pytest-3.2.5, py-1.4.34, pluggy-0.4.0
   rootdir: /home/user/.spack/extensions/spack-scripting, inifile: pytest.ini
   collected 5 items

   tests/test_filter.py ...XX
   ================================================================= short test summary info ==================================================================
   XPASS tests/test_filter.py::test_filtering_specs[flags3-specs3-expected3]
   XPASS tests/test_filter.py::test_filtering_specs[flags4-specs4-expected4]

   ================================================================ slowest 20 test durations =================================================================
   2.29s setup    tests/test_filter.py::test_filtering_specs[flags0-specs0-expected0]
   0.25s call     tests/test_filter.py::test_filtering_specs[flags3-specs3-expected3]
   0.21s call     tests/test_filter.py::test_filtering_specs[flags2-specs2-expected2]
   0.20s call     tests/test_filter.py::test_filtering_specs[flags1-specs1-expected1]
   0.19s call     tests/test_filter.py::test_filtering_specs[flags4-specs4-expected4]
   0.15s call     tests/test_filter.py::test_filtering_specs[flags0-specs0-expected0]
   0.00s setup    tests/test_filter.py::test_filtering_specs[flags2-specs2-expected2]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags4-specs4-expected4]
   0.00s setup    tests/test_filter.py::test_filtering_specs[flags3-specs3-expected3]
   0.00s setup    tests/test_filter.py::test_filtering_specs[flags4-specs4-expected4]
   0.00s setup    tests/test_filter.py::test_filtering_specs[flags1-specs1-expected1]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags0-specs0-expected0]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags1-specs1-expected1]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags2-specs2-expected2]
   0.00s teardown tests/test_filter.py::test_filtering_specs[flags3-specs3-expected3]
   =========================================================== 3 passed, 2 xpassed in 3.31 seconds ============================================================

-------------------
Updating extensions
-------------------

Finally it's possible to update extensions, e.g. to check out the latest version of
the code or switch to another branch or tag in the repository:

.. code-block:: console

   $ spack command-extensions update spack-scripting
   ==> Updating extension "spack-scripting" in the "user/linux" scope
   ==> Finished updating the "user/linux" scope

With any number of extension names specified, the ``update`` command updates
their code base by pulling the remote information. If no name is specified,
then the update is run on all the installed extensions. When updating or
getting an extension it's also possible to employ the ``@`` symbol to
specify the branch or tag to check out:

.. code-block:: console

   $ spack  command-extensions update spack-scripting@master
   ==> Updating extension "spack-scripting" in the "user/linux" scope [@master]
   ==> Finished updating the "user/linux" scope

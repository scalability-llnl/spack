@echo off
rem "C:\lib\spack\spack\test\data
rem
rem Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
rem Spack Project Developers. See the top-level COPYRIGHT file for details.
rem
rem SPDX-License-Identifier: (Apache-2.0 OR MIT)



rem Set an environment variable with some unicode in it to ensure that
rem Spack can decode it.
rem
rem This has caused squashed commits on develop to break, as some
rem committers use unicode in their messages, and Travis sets the
rem current commit message in an environment variable.
chcp 65001 > nul
set UNICODE_VAR=don\xe2\x80\x99t
chcp 437 > nul
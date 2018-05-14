#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, RunEnvironment, tools

class TestPackage(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def build(self):
        pass

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            self.run('ragel --version')

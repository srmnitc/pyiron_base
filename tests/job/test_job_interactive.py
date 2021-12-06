# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

import unittest
from pyiron_base.job.interactive import InteractiveBase
from pyiron_base._tests import TestWithProject


class TestJobInteractive(TestWithProject):
    def test_job_with(self):
        job = self.project.create_job(InteractiveBase, "test")
        with self.assertRaises(NotImplementedError):
            with job as _:
                pass
                
    def test_job_interactive_with(self):
        job = self.project.create_job(InteractiveBase, "interactive")
        with job.interactive_open() as _:
            pass

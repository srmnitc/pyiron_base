# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

import numpy as np
from pyiron_base.generic.units import PyironUnitRegistry, UnitConverter
import unittest
import pint

pint_registry = pint.UnitRegistry()


class TestUnits(unittest.TestCase):

    def test_units(self):
        base_units = PyironUnitRegistry()
        base_units.add_quantity(quantity="energy", unit=pint_registry.eV)
        self.assertRaises(ValueError, base_units.add_quantity, quantity="energy", unit="eV")
        dim_less_q = pint_registry.Quantity
        base_units.add_quantity(quantity="dimensionless_integer_quantity", unit=dim_less_q(1), data_type=int)
        code_units = PyironUnitRegistry()
        # Define unit kJ/mol
        code_units.add_quantity(quantity="energy",
                                unit=1e3 * pint_registry.cal / (pint_registry.mol * pint_registry.N_A))
        code_units.add_labels(labels=["energy_tot", "energy_pot"], quantity="energy")
        # Raise Error for undefined quantity
        self.assertRaises(ValueError, code_units.add_labels, labels=["mean_forces"], quantity="force")
        self.assertTrue(code_units["energy"], code_units["energy_tot"])
        self.assertTrue(code_units["energy"], code_units["energy_pot"])
        # Define converter
        unit_converter = UnitConverter(base_units=base_units, code_units=code_units)
        self.assertAlmostEqual(round(unit_converter.code_to_base_value("energy"), 3), 0.043)
        # Raise error if quantity not defined in any of the unit registries
        self.assertRaises(ValueError, unit_converter.code_to_base_value, "dimensionless_integer_quantity")
        self.assertRaises(ValueError, code_units.get_dtype, "dimensionless_integer_quantity")
        # Define dimensionless quantity in the code units registry
        code_units.add_quantity(quantity="dimensionless_integer_quantity", unit=dim_less_q(1), data_type=int)
        self.assertIsInstance(code_units.get_dtype("dimensionless_integer_quantity"), int.__class__)
        self.assertIsInstance(code_units.get_dtype("energy_tot"), float.__class__)
        self.assertAlmostEqual(unit_converter.code_to_base_value("dimensionless_integer_quantity"), 1)
        self.assertAlmostEqual(unit_converter.code_to_base_value("energy")
                               * unit_converter.base_to_code_value("energy"), 1e3)

        # Use decorator to convert units
        @unit_converter(quantity="energy", conversion="code_to_base")
        def return_ones_base():
            return np.ones(10)

        @unit_converter(quantity="energy", conversion="base_to_code")
        def return_ones_code():
            return np.ones(10)

        self.assertTrue(np.allclose(return_ones_base(), np.ones(10) * 0.0433641))
        self.assertTrue(np.allclose(return_ones_base() * return_ones_code(), np.ones(10) * 1e3))
        self.assertRaises(ValueError, unit_converter, quantity="energy", conversion="gibberish")
        # Define dimensionally incorrect units
        code_units.add_quantity(quantity="energy",
                                unit=pint_registry.N * pint_registry.metre ** 2)
        unit_converter = UnitConverter(base_units=base_units, code_units=code_units)
        # Check if dimensionality error raised
        self.assertRaises(pint.DimensionalityError, unit_converter.code_to_base_value, "energy")
        # Try SI units
        code_units.add_quantity(quantity="energy",
                                unit=pint_registry.N * pint_registry.metre)
        unit_converter = UnitConverter(base_units=base_units, code_units=code_units)
        self.assertAlmostEqual(round(unit_converter.code_to_base_value("energy") / 1e18, 3), 6.242)

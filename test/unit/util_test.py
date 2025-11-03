import unittest
import pytest

from app import util


@pytest.mark.unit
class TestUtil(unittest.TestCase):
    def test_convert_to_number_correct_param(self):
        self.assertEqual(4, util.convert_to_number("4"))
        self.assertEqual(0, util.convert_to_number("0"))
        self.assertEqual(0, util.convert_to_number("-0"))
        self.assertEqual(-1, util.convert_to_number("-1"))
        self.assertEqual(5, util.convert_to_number("+5"))
        self.assertEqual(5, util.convert_to_number("0005"))
        self.assertEqual(5, util.convert_to_number(" 5"))
        self.assertEqual(5, util.convert_to_number("5 "))
        self.assertAlmostEqual(4.0, util.convert_to_number("4.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("0.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("-0.0"), delta=0.0000001)
        self.assertAlmostEqual(-1.0, util.convert_to_number("-1.0"), delta=0.0000001)
        self.assertAlmostEqual(3.14, util.convert_to_number("+3.14"), delta=0.0000001)
        self.assertAlmostEqual(5.0, util.convert_to_number("5."), delta=0.0000001)
        self.assertAlmostEqual(0.5, util.convert_to_number(".5"), delta=0.0000001)

    def test_convert_to_number_invalid_type(self):
        self.assertRaises(TypeError, util.convert_to_number, "")
        self.assertRaises(TypeError, util.convert_to_number, "3.h")
        self.assertRaises(TypeError, util.convert_to_number, "s")
        self.assertRaises(TypeError, util.convert_to_number, None)
        self.assertRaises(TypeError, util.convert_to_number, object())
        self.assertRaises(TypeError, util.convert_to_number, "3.14.15")
        self.assertRaises(TypeError, util.convert_to_number, "..5")
        self.assertRaises(TypeError, util.convert_to_number, True)
        self.assertRaises(TypeError, util.convert_to_number, False)

    def test_validate_permissions_success(self):
        """Prueba que user1 tenga permisos para cualquier operación"""
        self.assertTrue(util.validate_permissions("2 + 3", "user1"))
        self.assertTrue(util.validate_permissions("10 / 2", "user1"))
        self.assertTrue(util.validate_permissions("sqrt(16)", "user1"))

    def test_validate_permissions_failure(self):
        """Prueba que otros usuarios NO tengan permisos"""
        self.assertFalse(util.validate_permissions("2 + 3", "user2"))
        self.assertFalse(util.validate_permissions("10 / 2", "admin"))
        self.assertFalse(util.validate_permissions("sqrt(16)", "guest"))
        self.assertFalse(util.validate_permissions("2 * 3", ""))
        self.assertFalse(util.validate_permissions("2 * 3", None))

    def test_validate_permissions_different_operations(self):
        """Prueba que la operación no afecta el resultado, solo el usuario"""
        self.assertTrue(util.validate_permissions("cualquier operación", "user1"))
        self.assertFalse(util.validate_permissions("cualquier operación", "user2"))
import unittest
import math
from unittest.mock import patch
import pytest

from app.calc import Calculator


def mocked_validation(*args, **kwargs):
    return True


@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_add_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(4, self.calc.add(2, 2))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_substract_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(0, self.calc.substract(2, 2))
        self.assertEqual(4, self.calc.substract(2, -2))
        self.assertEqual(-4, self.calc.substract(-2, 2))
        self.assertEqual(5, self.calc.substract(10, 5))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(4, self.calc.multiply(2, 2))
        self.assertEqual(0, self.calc.multiply(1, 0))
        self.assertEqual(0, self.calc.multiply(-1, 0))
        self.assertEqual(-2, self.calc.multiply(-1, 2))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_divide_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))
        self.assertEqual(2.5, self.calc.divide(5, 2))
        self.assertEqual(-2, self.calc.divide(-4, 2))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_power_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(8, self.calc.power(2, 3))
        self.assertEqual(1, self.calc.power(5, 0))
        self.assertEqual(25, self.calc.power(5, 2))
        self.assertEqual(0.25, self.calc.power(2, -2))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_square_root_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(4, self.calc.square_root(16))
        self.assertEqual(5, self.calc.square_root(25))
        self.assertEqual(0, self.calc.square_root(0))
        self.assertEqual(math.sqrt(2), self.calc.square_root(2))

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_logarithm_base_10_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(2, self.calc.logarithm_base_10(100))
        self.assertEqual(3, self.calc.logarithm_base_10(1000))
        self.assertEqual(0, self.calc.logarithm_base_10(1))
        self.assertEqual(math.log10(5), self.calc.logarithm_base_10(5))

    # TESTS DE ERRORES 
    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_add_method_fails_with_nan_parameter(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.add, "2", 2)
        self.assertRaises(TypeError, self.calc.add, 2, "2")
        self.assertRaises(TypeError, self.calc.add, "2", "2")
        self.assertRaises(TypeError, self.calc.add, None, 2)
        self.assertRaises(TypeError, self.calc.add, 2, None)
        self.assertRaises(TypeError, self.calc.add, object(), 2)
        self.assertRaises(TypeError, self.calc.add, [1, 2], 2)
        self.assertRaises(TypeError, self.calc.add, {"a": 1}, 2)

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_substract_method_fails_with_nan_parameter(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.substract, "2", 2)
        self.assertRaises(TypeError, self.calc.substract, 2, "2")
        self.assertRaises(TypeError, self.calc.substract, "2", "2")
        self.assertRaises(TypeError, self.calc.substract, None, 2)
        self.assertRaises(TypeError, self.calc.substract, 2, None)
        self.assertRaises(TypeError, self.calc.substract, object(), 2)
        self.assertRaises(TypeError, self.calc.substract, [1, 2], 2)

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_fails_with_nan_parameter(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.multiply, "2", 2)
        self.assertRaises(TypeError, self.calc.multiply, 2, "2")
        self.assertRaises(TypeError, self.calc.multiply, "2", "2")
        self.assertRaises(TypeError, self.calc.multiply, None, 2)
        self.assertRaises(TypeError, self.calc.multiply, 2, None)
        self.assertRaises(TypeError, self.calc.multiply, object(), 2)
        self.assertRaises(TypeError, self.calc.multiply, [1, 2], 2)
        self.assertRaises(TypeError, self.calc.multiply, {"a": 1}, 2)

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_divide_method_fails_with_nan_parameter(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")
        self.assertRaises(TypeError, self.calc.divide, None, 2)
        self.assertRaises(TypeError, self.calc.divide, 2, None)
        self.assertRaises(TypeError, self.calc.divide, object(), 2)
        self.assertRaises(TypeError, self.calc.divide, [1, 2], 2)
    
    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_power_method_fails_with_nan_parameter(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.power, "2", 2)
        self.assertRaises(TypeError, self.calc.power, 2, "2")
        self.assertRaises(TypeError, self.calc.power, "2", "2")
        self.assertRaises(TypeError, self.calc.power, None, 2)
        self.assertRaises(TypeError, self.calc.power, 2, None)
        self.assertRaises(TypeError, self.calc.power, object(), 2)
        self.assertRaises(TypeError, self.calc.power, [1, 2], 2)
    
    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_square_root_method_fails_with_nan_parameter(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.square_root, "2")
        self.assertRaises(TypeError, self.calc.square_root, None)
        self.assertRaises(TypeError, self.calc.square_root, object())
        self.assertRaises(TypeError, self.calc.square_root, [1, 2])

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_logarithm_method_fails_with_nan_parameter(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.logarithm_base_10, "2")
        self.assertRaises(TypeError, self.calc.logarithm_base_10, None)
        self.assertRaises(TypeError, self.calc.logarithm_base_10, object())
        self.assertRaises(TypeError, self.calc.logarithm_base_10, [1, 2])

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_divide_method_fails_with_division_by_zero(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.divide, 2, 0)
        self.assertRaises(TypeError, self.calc.divide, 2, -0)
        self.assertRaises(TypeError, self.calc.divide, 0, 0)

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_square_root_method_fails_with_negative_number(self, _validate_permissions):
        self.assertRaises(ValueError, self.calc.square_root, -4)
        self.assertRaises(ValueError, self.calc.square_root, -1)

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_logarithm_method_fails_with_invalid_numbers(self, _validate_permissions):
        self.assertRaises(ValueError, self.calc.logarithm_base_10, 0)
        self.assertRaises(ValueError, self.calc.logarithm_base_10, -5)
        self.assertRaises(ValueError, self.calc.logarithm_base_10, -1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

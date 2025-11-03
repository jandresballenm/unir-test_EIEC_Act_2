import http.client
import os
import unittest
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    # ========== PRUEBAS PARA SUMA ==========
    def test_api_add_success(self):
        """Prueba suma exitosa con diferentes casos"""
        # Caso 1: Suma básica
        url = f"{BASE_URL}/calc/add/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "4")
        
        # Caso 2: Suma con números negativos
        url = f"{BASE_URL}/calc/add/5/-3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "2")
        
        # Caso 3: Suma con cero
        url = f"{BASE_URL}/calc/add/0/7"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "7")

    def test_api_add_invalid_parameters(self):
        """Prueba parámetros inválidos que deben retornar 400 Bad Request"""
        # Caso 1: Parámetro no numérico
        url = f"{BASE_URL}/calc/add/abc/2"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST, f"Debería ser 400 Bad Request para {url}")
        
        # Caso 2: Ambos parámetros no numéricos
        url = f"{BASE_URL}/calc/add/xyz/abc"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(e.code, http.client.BAD_REQUEST, f"Debería ser 400 Bad Request para {url}")

    def test_api_add_decimal_numbers(self):
        """Prueba suma con números decimales"""
        url = f"{BASE_URL}/calc/add/2.5/1.5"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "4.0")
        
        url = f"{BASE_URL}/calc/add/0.1/0.2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertAlmostEqual(float(result), 0.3, places=5)

    def test_api_add_large_numbers(self):
        """Prueba suma con números grandes"""
        url = f"{BASE_URL}/calc/add/999999/1"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "1000000")

    def test_api_add_response_headers(self):
        """Prueba que los headers de respuesta sean correctos"""
        url = f"{BASE_URL}/calc/add/3/4"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        
        # Verificar headers importantes
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'text/plain')
        
        # Verificar CORS headers
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        self.assertEqual(cors_header, '*')

    def test_api_add_method_not_allowed(self):
        """Prueba métodos HTTP no permitidos"""
        url = f"{BASE_URL}/calc/add/2/2"
        
        # Intentar POST en lugar de GET
        try:
            request = Request(url, method='POST')
            urlopen(request, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.METHOD_NOT_ALLOWED, 
                f"Debería ser 405 Method Not Allowed para {url}"
            )

    # ========== PRUEBAS PARA RESTA ==========
    def test_api_substract_success(self):
        """Prueba resta exitosa con diferentes casos"""
        # Caso 1: Resta básica
        url = f"{BASE_URL}/calc/substract/5/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "2")
        
        # Caso 2: Resta con números negativos
        url = f"{BASE_URL}/calc/substract/5/-3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "8")
        
        # Caso 3: Resta con cero
        url = f"{BASE_URL}/calc/substract/7/0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "7")

    def test_api_substract_invalid_parameters(self):
        """Prueba parámetros inválidos para resta"""
        url = f"{BASE_URL}/calc/substract/abc/2"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_substract_decimal_numbers(self):
        """Prueba resta con números decimales"""
        url = f"{BASE_URL}/calc/substract/5.5/2.2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertAlmostEqual(float(result), 3.3, places=5)

    def test_api_substract_large_numbers(self):
        """Prueba resta con números grandes"""
        url = f"{BASE_URL}/calc/substract/1000000/1"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "999999")

    def test_api_substract_response_headers(self):
        """Prueba headers de respuesta para resta"""
        url = f"{BASE_URL}/calc/substract/8/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'text/plain')
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        self.assertEqual(cors_header, '*')

    def test_api_substract_method_not_allowed(self):
        """Prueba métodos HTTP no permitidos para resta"""
        url = f"{BASE_URL}/calc/substract/5/3"
        try:
            request = Request(url, method='POST')
            urlopen(request, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.METHOD_NOT_ALLOWED, 
                f"Debería ser 405 Method Not Allowed para {url}"
            )

    # ========== PRUEBAS PARA MULTIPLICACIÓN ==========
    def test_api_multiply_success(self):
        """Prueba multiplicación exitosa con diferentes casos"""
        # Caso 1: Multiplicación básica
        url = f"{BASE_URL}/calc/multiply/4/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "12")
        
        # Caso 2: Multiplicación con negativos
        url = f"{BASE_URL}/calc/multiply/5/-2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "-10")
        
        # Caso 3: Multiplicación con cero
        url = f"{BASE_URL}/calc/multiply/7/0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "0")

    def test_api_multiply_invalid_parameters(self):
        """Prueba parámetros inválidos para multiplicación"""
        url = f"{BASE_URL}/calc/multiply/abc/2"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_multiply_decimal_numbers(self):
        """Prueba multiplicación con números decimales"""
        url = f"{BASE_URL}/calc/multiply/2.5/4.0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "10.0")

    def test_api_multiply_large_numbers(self):
        """Prueba multiplicación con números grandes"""
        url = f"{BASE_URL}/calc/multiply/1000/1000"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "1000000")

    def test_api_multiply_response_headers(self):
        """Prueba headers de respuesta para multiplicación"""
        url = f"{BASE_URL}/calc/multiply/6/7"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'text/plain')
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        self.assertEqual(cors_header, '*')

    def test_api_multiply_method_not_allowed(self):
        """Prueba métodos HTTP no permitidos para multiplicación"""
        url = f"{BASE_URL}/calc/multiply/4/3"
        try:
            request = Request(url, method='POST')
            urlopen(request, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.METHOD_NOT_ALLOWED, 
                f"Debería ser 405 Method Not Allowed para {url}"
            )

    # ========== PRUEBAS PARA DIVISIÓN ==========
    def test_api_divide_success(self):
        """Prueba división exitosa con diferentes casos"""
        # Caso 1: División básica
        url = f"{BASE_URL}/calc/divide/10/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "5.0")
        
        # Caso 2: División con decimales
        url = f"{BASE_URL}/calc/divide/5/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "2.5")
        
        # Caso 3: División con números negativos
        url = f"{BASE_URL}/calc/divide/-10/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "-5.0")

    def test_api_divide_invalid_parameters(self):
        """Prueba parámetros inválidos para división"""
        url = f"{BASE_URL}/calc/divide/abc/2"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_divide_decimal_numbers(self):
        """Prueba división con números decimales"""
        url = f"{BASE_URL}/calc/divide/5.5/2.0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "2.75")

    def test_api_divide_large_numbers(self):
        """Prueba división con números grandes"""
        url = f"{BASE_URL}/calc/divide/1000000/1000"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "1000.0")

    def test_api_divide_by_zero(self):
        """Prueba división por cero"""
        url = f"{BASE_URL}/calc/divide/10/0"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_divide_response_headers(self):
        """Prueba headers de respuesta para división"""
        url = f"{BASE_URL}/calc/divide/15/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'text/plain')
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        self.assertEqual(cors_header, '*')

    def test_api_divide_method_not_allowed(self):
        """Prueba métodos HTTP no permitidos para división"""
        url = f"{BASE_URL}/calc/divide/10/2"
        try:
            request = Request(url, method='POST')
            urlopen(request, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.METHOD_NOT_ALLOWED, 
                f"Debería ser 405 Method Not Allowed para {url}"
            )

    # ========== PRUEBAS PARA POTENCIA ==========
    def test_api_power_success(self):
        """Prueba potencia exitosa con diferentes casos"""
        # Caso 1: Potencia básica
        url = f"{BASE_URL}/calc/power/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "8")
        
        # Caso 2: Potencia con exponente cero
        url = f"{BASE_URL}/calc/power/5/0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "1")
        
        # Caso 3: Potencia con base negativa
        url = f"{BASE_URL}/calc/power/-2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "-8")

    def test_api_power_invalid_parameters(self):
        """Prueba parámetros inválidos para potencia"""
        url = f"{BASE_URL}/calc/power/abc/2"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_power_decimal_numbers(self):
        """Prueba potencia con números decimales"""
        url = f"{BASE_URL}/calc/power/4/0.5"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "2.0")

    def test_api_power_large_numbers(self):
        """Prueba potencia con números grandes"""
        url = f"{BASE_URL}/calc/power/10/6"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "1000000")

    def test_api_power_response_headers(self):
        """Prueba headers de respuesta para potencia"""
        url = f"{BASE_URL}/calc/power/3/4"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'text/plain')
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        self.assertEqual(cors_header, '*')

    def test_api_power_method_not_allowed(self):
        """Prueba métodos HTTP no permitidos para potencia"""
        url = f"{BASE_URL}/calc/power/2/3"
        try:
            request = Request(url, method='POST')
            urlopen(request, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.METHOD_NOT_ALLOWED, 
                f"Debería ser 405 Method Not Allowed para {url}"
            )

    # ========== PRUEBAS PARA RAÍZ CUADRADA ==========
    def test_api_sqrt_success(self):
        """Prueba raíz cuadrada exitosa con diferentes casos"""
        # Caso 1: Raíz cuadrada básica
        url = f"{BASE_URL}/calc/sqrt/9"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "3.0")
        
        # Caso 2: Raíz cuadrada con decimales
        url = f"{BASE_URL}/calc/sqrt/2.25"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "1.5")
        
        # Caso 3: Raíz cuadrada de cero
        url = f"{BASE_URL}/calc/sqrt/0"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "0.0")

    def test_api_sqrt_invalid_parameters(self):
        """Prueba parámetros inválidos para raíz cuadrada"""
        url = f"{BASE_URL}/calc/sqrt/abc"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_sqrt_negative_number(self):
        """Prueba raíz cuadrada de número negativo"""
        url = f"{BASE_URL}/calc/sqrt/-9"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_sqrt_response_headers(self):
        """Prueba headers de respuesta para raíz cuadrada"""
        url = f"{BASE_URL}/calc/sqrt/16"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'text/plain')
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        self.assertEqual(cors_header, '*')

    def test_api_sqrt_method_not_allowed(self):
        """Prueba métodos HTTP no permitidos para raíz cuadrada"""
        url = f"{BASE_URL}/calc/sqrt/25"
        try:
            request = Request(url, method='POST')
            urlopen(request, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.METHOD_NOT_ALLOWED, 
                f"Debería ser 405 Method Not Allowed para {url}"
            )

    # ========== PRUEBAS PARA LOGARITMO BASE 10 ==========
    def test_api_log10_success(self):
        """Prueba logaritmo base 10 exitoso con diferentes casos"""
        # Caso 1: Logaritmo básico
        url = f"{BASE_URL}/calc/log10/100"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "2.0")
        
        # Caso 2: Logaritmo de 1
        url = f"{BASE_URL}/calc/log10/1"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "0.0")
        
        # Caso 3: Logaritmo de número decimal
        url = f"{BASE_URL}/calc/log10/10"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        result = response.read().decode('utf-8')
        self.assertEqual(result, "1.0")

    def test_api_log10_invalid_parameters(self):
        """Prueba parámetros inválidos para logaritmo"""
        url = f"{BASE_URL}/calc/log10/abc"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_log10_invalid_values(self):
        """Prueba logaritmo de valores no permitidos"""
        # Caso 1: Logaritmo de cero
        url = f"{BASE_URL}/calc/log10/0"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )
        
        # Caso 2: Logaritmo de número negativo
        url = f"{BASE_URL}/calc/log10/-5"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.BAD_REQUEST, 
                f"Debería ser 400 Bad Request para {url}"
            )

    def test_api_log10_response_headers(self):
        """Prueba headers de respuesta para logaritmo"""
        url = f"{BASE_URL}/calc/log10/1000"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'text/plain')
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        self.assertEqual(cors_header, '*')

    def test_api_log10_method_not_allowed(self):
        """Prueba métodos HTTP no permitidos para logaritmo"""
        url = f"{BASE_URL}/calc/log10/100"
        try:
            request = Request(url, method='POST')
            urlopen(request, timeout=DEFAULT_TIMEOUT)
            self.fail("Debería haber lanzado HTTPError")
        except HTTPError as e:
            self.assertEqual(
                e.code, http.client.METHOD_NOT_ALLOWED, 
                f"Debería ser 405 Method Not Allowed para {url}"
            )

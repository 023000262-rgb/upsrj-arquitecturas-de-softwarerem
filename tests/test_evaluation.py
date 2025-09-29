# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: test_evaluation.py
# Descripción: Archivo de pruebas unitarias para validar el comportamiento de funciones del proyecto
# ============================================================
import sys, os, unittest, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main

# Colores ANSI
GREEN = "\033[92m"
RED = "\033[91m"
LIGHT_RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1m"
SEPARATOR = f"{BOLD}{'='*50}{RESET}"

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append((test))

class CustomTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)
    
class TestEvaluation(unittest.TestCase):
    
    def test_suma_basica(self):
        """Verifica que suma(3, 5) devuelve 8"""
        resultado = main.suma(3, 5)
        self.assertEqual(resultado, 8)

    def test_suma_negativos(self):
        """Verifica que suma(-2, -3) devuelve -5"""
        resultado = main.suma(-2, -3)
        self.assertEqual(resultado, -5)

    def test_suma_mixta(self):
        """Verifica que suma(-4, 10) devuelve 6"""
        resultado = main.suma(-4, 10)
        self.assertEqual(resultado, 6)

    def test_main_status(self):
        """Verifica que main() retorna os.EX_OK"""
        status = main.main()
        self.assertEqual(status, os.EX_OK)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEvaluation)
    silent_stream = io.StringIO()
    runner = CustomTestRunner(stream=silent_stream, verbosity=0)
    result = runner.run(suite)

    print(f"{BOLD}EVALUACION{RESET}")
    # Resultados individuales
    print(SEPARATOR)
    print(f"{BOLD}Resultados individuales:{RESET}")
    for test_case in result.successes:
        print(f"{test_case._testMethodName}: {GREEN}{BOLD}PASSED{RESET}")

    for test_case, traceback in result.failures + result.errors:
        print(f"{test_case._testMethodName}: {RED}{BOLD}FAILED{RESET}")
        # Extraer solo el mensaje de la última línea del traceback
        last_line = traceback.strip().split('\n')[-1]
        mensaje = last_line.split(':')[-1].strip()
        print(f"- detalles: {LIGHT_RED}{mensaje}{RESET}")

    # Resumen final
    print(SEPARATOR)
    print(f"{BOLD}Resumen final:{RESET}")
    if result.wasSuccessful():
        print(f"{GREEN}{BOLD}SUCCESS:{RESET} Todos los tests pasaron correctamente.")
    else:
        print(f"{RED}{BOLD}FAILED:{RESET} Uno o más tests fallaron.")
    print(SEPARATOR)

    sys.exit(not result.wasSuccessful())
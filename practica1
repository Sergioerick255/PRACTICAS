def validar_parentesis(cadena):
    """Verifica si los paréntesis en la cadena están bien formados.
    Args:
        cadena (str): La cadena de entrada que contiene solo '(' y ')'.
    Returns:
        bool: True si los paréntesis están bien formados, False de lo contrario."""

    pila = []

    for caracter in cadena:
        if caracter == '(':
            pila.append(caracter)
        elif caracter == ')':
            if not pila:
                print("Rechazado: Se encontró un ')' sin un '(' correspondiente.")
                return False
            pila.pop()

    if pila:
        print("Rechazado: No todos los '(' tienen un ')' correspondiente.")
        return False
    return True

def solicitar_cadena():
    """Solicita al usuario que introduzca una cadena con solo paréntesis '()' y valida el input."""
    while True:
        cadena= input("Por favor, introduce una cadena con solo paréntesis '()' para validar: ")
        if not set(cadena).issubset({'(', ')'}):
            print("Error: la cadena contiene caracteres no permitidos. Introduce solo paréntesis.")
        elif not validar_parentesis(cadena):
            print("Los paréntesis no están bien formados. Asegúrate de cerrar todos los paréntesis abiertos.")
        else:
            print("La cadena de paréntesis está bien formada.")
            break

solicitar_cadena()

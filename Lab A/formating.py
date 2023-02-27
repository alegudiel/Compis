def cleanRegex(r):
    # Eliminar espacios en blanco
    r = r.replace(" ", "")

    # Reemplazar el operador '?' por el símbolo de epsilon
    r = r.replace("?", "ε")

    # Manejar el operador '+' como una operación kleene
    formatingRegex = ""
    i = 0
    while i < len(r):
        # Manejar el operador '+'
        if r[i] == "+":
            # Revisar si el caracter anterior es un paréntesis derecho o un caracter
            prev_char = formatingRegex[-1] if len(formatingRegex) > 0 else None
            if prev_char == ")" or prev_char.isalpha():
                formatingRegex += "*"
            # Agregar el caracter actual
            formatingRegex += r[i]
            i += 1
        # Agregar el operador '.' si es necesario
        elif i > 0 and r[i] not in "|*+)" and r[i-1] not in "|*+(":
            formatingRegex += "."
        # Agregar el caracter actual
        formatingRegex += r[i]
        i += 1

    return formatingRegex

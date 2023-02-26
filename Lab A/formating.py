def cleanRegex(regex):
    """
    Formatea una expresión regular para ser procesada a postfix.
    """

    # Agregar un punto explícito en concatenaciones implícitas
    formatingRegex = ""
    for i in range(len(regex)):
        if i > 0 and regex[i] not in "|*+)" and regex[i-1] not in "|*+(":
            formatingRegex += "."
        formatingRegex += regex[i]

    # Reemplazar las llaves por símbolos de repetición
    formatingRegex = formatingRegex.replace("{", "{1,")
    formatingRegex = formatingRegex.replace(",}", ",}")
    formatingRegex = formatingRegex.replace(",", "}")
    formatingRegex = formatingRegex.replace("}", "}")

    return formatingRegex

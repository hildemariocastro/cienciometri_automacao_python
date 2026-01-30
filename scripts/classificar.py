def classificar_artigo(texto):
    categorias = {
        "histologia": ["histology", "histological"],
        "aquicultura": ["aquaculture", "shrimp", "fish"],
        "machine_learning": ["machine learning", "deep learning", "cnn"]
    }

    tecnicas = {
        "h&e": ["hematoxylin", "h&e"],
        "ihq": ["immunohistochemistry"],
        "histochemistry": ["pas", "alcian"]
    }

    resultado = {
        "categoria": "outros",
        "tecnica": "nao_identificada",
        "status_prisma": "excluir"
    }

    for cat, palavras in categorias.items():
        if any(p in texto for p in palavras):
            resultado["categoria"] = cat
            resultado["status_prisma"] = "incluir"

    for tec, palavras in tecnicas.items():
        if any(p in texto for p in palavras):
            resultado["tecnica"] = tec

    return resultado


def classificar_resumo(titulo, resumo):
    texto = f"{titulo} {resumo}".lower()
    return classificar_artigo(texto)

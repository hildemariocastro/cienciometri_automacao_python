import pandas as pd

ENTRADA = "data/banco_classificado.csv"
SAIDA = "data/tabela_prisma.csv"

df = pd.read_csv(ENTRADA)

prisma = {
    "Registros identificados (total)": len(df),

    "DOI ausente": (df["status_download"] == "doi_ausente").sum(),
    "Falha técnica (API/download)": df["status_download"].str.contains("erro", na=False).sum(),

    "Registros após triagem técnica": (
        (~df["status_download"].isin(["doi_ausente"])) &
        (~df["status_download"].str.contains("erro", na=False))
    ).sum(),

    "Texto completo disponível": (df["nivel_informacao"] == "texto_completo").sum(),
    "Apenas resumo analisado": (df["nivel_informacao"] == "resumo").sum(),

    "Estudos incluídos (PRISMA)": (df["status_prisma"] == "incluir").sum(),
    "Estudos excluídos": (df["status_prisma"] == "excluir").sum()
}

tabela_prisma = pd.DataFrame(
    prisma.items(),
    columns=["Etapa PRISMA", "Número de artigos"]
)

tabela_prisma.to_csv(SAIDA, index=False)

print("✅ Tabela PRISMA gerada com sucesso")

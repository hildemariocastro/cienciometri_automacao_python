import pandas as pd
from resolver_doi import resolver_doi
from extrair_texto import extrair_texto_pdf
from classificar import classificar_artigo, classificar_resumo

ENTRADA = "data/metadados.csv"
SAIDA = "data/banco_classificado.csv"

df = pd.read_csv(ENTRADA)

resultados = []

for _, row in df.iterrows():
    doi = row.get("doi", "")
    titulo = row.get("title", "")
    resumo = row.get("abstract", "")

    pdf_path, status_download = resolver_doi(doi)

    if pdf_path:
        texto = extrair_texto_pdf(pdf_path)
        classificacao = classificar_artigo(texto)
        nivel = "texto_completo"
    else:
        classificacao = classificar_resumo(titulo, resumo)
        nivel = "resumo"

    resultados.append({
        **row.to_dict(),
        "status_download": status_download,
        "nivel_informacao": nivel,
        **classificacao
    })

df_final = pd.DataFrame(resultados)
df_final.to_csv(SAIDA, index=False)

print("✅ Pipeline concluído com sucesso")


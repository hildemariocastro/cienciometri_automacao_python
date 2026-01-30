import chardet

arquivo = "data/banco_classificado.csv"

with open(arquivo, "rb") as f:
    raw = f.read(100000)

resultado = chardet.detect(raw)
print(resultado)

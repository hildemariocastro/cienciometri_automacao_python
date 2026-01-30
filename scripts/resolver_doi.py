import requests
import os

UNPAYWALL_EMAIL = "hildemario.castro@ufrpe.br"

def resolver_doi(doi, pasta_pdfs="pdfs"):
    if not doi or doi == "":
        return None, "doi_ausente"

    url = f"https://api.unpaywall.org/v2/{doi}?email={UNPAYWALL_EMAIL}"

    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            return None, "erro_api"

        data = r.json()

        if not data.get("is_oa"):
            return None, "sem_open_access"

        pdf_url = data.get("best_oa_location", {}).get("url_for_pdf")
        if not pdf_url:
            return None, "sem_pdf"

        os.makedirs(pasta_pdfs, exist_ok=True)
        pdf_path = os.path.join(pasta_pdfs, doi.replace("/", "_") + ".pdf")

        pdf = requests.get(pdf_url, timeout=30)
        if pdf.status_code == 200:
            with open(pdf_path, "wb") as f:
                f.write(pdf.content)
            return pdf_path, "download_ok"
        else:
            return None, "erro_download"

    except Exception:
        return None, "erro_execucao"

import re

def extrair_emails(texto):
    
    padrao_email = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails_encontrados = re.findall(padrao_email, texto)
    return ' '.join(emails_encontrados)

if __name__ == "__main__":
    texto_exemplo = "Favor enviar um e-mail para abc@hotmail.com com cópia para def@abc.com.br"
    print(extrair_emails(texto_exemplo))

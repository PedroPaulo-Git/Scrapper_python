import pyotp
import time

def get_2fa_code():
    # Definindo o segredo diretamente aqui (não precisa passar como argumento)
    secret = "M4G5A5OV57UPCVCKEGXUHDOOJDMQHBKP"  # Substitua pelo segredo real
    totp = pyotp.TOTP(secret)
    return totp.now()

# Exemplo de uso, imprimindo o código a cada 30 segundos
if __name__ == "__main__":
    while True:
        print(f"Código TOTP: {get_2fa_code()}")
        time.sleep(30)  # Espera 30 segundos até gerar um novo código

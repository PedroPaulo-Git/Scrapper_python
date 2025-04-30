import os
import time
from instaloader import Instaloader
from instaloader.exceptions import TwoFactorAuthRequiredException
from routes.getcode2fa import get_2fa_code
def login_instaloader(username, password, max_retries=3):
    try:
        L = Instaloader()
        session_filename = f"session-{username}"

        # Tentando carregar a sessão salva, se existir
        try:
            print("Tentando carregar a sessão...")
            L.load_session_from_file(username, session_filename)
            print(f"Sessão carregada com sucesso para {username}.")
            return L  # Sessão carregada com sucesso, não precisa logar de novo
        except FileNotFoundError:
            print("Nenhuma sessão encontrada. Realizando login...")

        # Realiza o login
        try:
            print("Tentando login sem 2FA...")
            L.login(username, password)
            print(f"Login bem-sucedido com {username} sem 2FA.")
        except TwoFactorAuthRequiredException:
            print("2FA requerido! Obtendo código...")

            for attempt in range(1, max_retries + 1):
                print(f"Tentativa {attempt} para obter código 2FA...")
                code = get_2fa_code()
                if code:
                    print(f"Autenticando com o código 2FA: {code}")
                    try:
                        L.two_factor_login(code)
                        print(f"Login bem-sucedido com {username} usando 2FA.")
                        break
                    except Exception as e:
                        print(f"Erro durante o login com o código 2FA: {str(e)}")
                        if attempt == max_retries:
                            print("Número máximo de tentativas alcançado.")
                else:
                    print("Código 2FA não encontrado. Tentando novamente...")
                time.sleep(5)

        # Salvando a sessão
        print("Salvando a sessão...")
        L.save_session_to_file(session_filename)
        print("Sessão salva com sucesso!")
        return L

    except Exception as e:
        print(f"Erro durante o login: {str(e)}")
        raise

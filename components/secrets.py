import os
from typing import Union

from components.logger import logger


def get_secret(secret_key: str) -> Union[str, bool]:
    """
    Recupera uma "secret" (segredo) a partir de uma variável de ambiente ou de um arquivo.
    Fluxo:
    1. Se secret_key for falsy (None, string vazia, etc.), registra um erro e retorna False.
    2. Verifica se existe uma variável de ambiente com o nome secret_key:
        - se existir (ou seja, os.getenv(secret_key) não é None), retorna o valor (pode ser string vazia).
    3. Caso contrário, tenta abrir o arquivo 'private/{secret_key}' relativo ao diretório de trabalho atual:
        - se o arquivo existir, lê seu conteúdo, faz strip() e retorna a string resultante.
        - se o arquivo não for encontrado, registra erro e retorna False.
        - em caso de qualquer outra exceção ao abrir/ler, registra o erro com a exceção e retorna False.
    Parâmetros:
         secret_key (str): Nome da chave/arquivo a ser buscado. Deve ser uma string representando o nome da variável de ambiente ou o nome do arquivo dentro do diretório 'private'.
    Retorno:
         Union[str, bool]:
              - str: o segredo encontrado (valor da variável de ambiente ou conteúdo do arquivo, com espaços em branco nas extremidades removidos).
              - False: em caso de erro, chave não fornecida, arquivo não encontrado ou outra exceção durante a leitura.
    Efeitos colaterais:
         - Registra mensagens de debug e erro usando o logger (por exemplo: "encontrada com sucesso", "não encontrado", "Erro ao tentar abrir ...").
         - Lê arquivos do sistema de arquivos (diretório 'private').
    Observações:
         - Uma variável de ambiente definida com valor vazio será considerada presente e retornará a string vazia.
         - O caminho do arquivo é formado sem validação adicional: 'private/{secret_key}'.
         - Não lança exceções externas; todos os erros são tratados internamente e resultam em retorno False.
    Exemplo de uso:
         secret = get_secret("MY_SECRET")
         if secret is not False:
              # usar o segredo
         else:
              # tratar erro / segredo não encontrado
    """

    # Validando que recebeu uma secret key
    if not secret_key:

        logger.error("Chave de senha não fornecida")

        return False

    if os.getenv(secret_key) is not None:

        logger.debug(f"{secret_key} encontrada com sucesso")

        return os.getenv(secret_key)

    try:

        with open(f"private/{secret_key}") as f:

            logger.debug(f"{secret_key} encontrada com sucesso")

            return f.read().strip()

    except FileNotFoundError:

        logger.error(f"{secret_key} não encontrado")

        return False

    except Exception as e:

        logger.error(f"Erro ao tentar abrir {secret_key}: {e}")

        return False

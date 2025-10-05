import argparse
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent[3]

MAX_BYTES = 2_000_000  # 2MB


def secure_path(rel: str) -> Path:
    """
    Retorna um objeto pathlib.Path resolvido para um caminho relativo ao WORKSPACE_ROOT,
    garantindo que o resultado permaneça dentro do diretório raiz do workspace.

    Args:
        rel (str): Caminho relativo (ou subcaminho) a partir de WORKSPACE_ROOT.

    Returns:
        pathlib.Path: Caminho absoluto e canônico correspondente a WORKSPACE_ROOT / rel.

    Comportamento e efeitos colaterais:
        - Concatena WORKSPACE_ROOT com o argumento rel e chama .resolve() para obter o caminho absoluto.
        - Se o caminho resolvido não começar com WORKSPACE_ROOT, grava uma mensagem de erro em sys.stderr
          e encerra o processo com sys.exit(1) (isto previne travessias de diretório fora do workspace).
        - Depende de variáveis/globals do módulo (por exemplo WORKSPACE_ROOT) e do módulo sys.

    Erros:
        - A função não lança uma exceção para o caso de caminho fora do workspace; em vez disso finaliza o processo.
        - A chamada .resolve() pode propagar exceções relacionadas ao sistema de arquivos (por exemplo, problemas de permissão);
          tais exceções não são tratadas pela função.

    Exemplo:
        >>> secure_path('subdir/arquivo.txt')
        PosixPath('/caminho/absoluto/para/workspace/subdir/arquivo.txt')
    """
    p = (WORKSPACE_ROOT / rel).resolve()
    if not str(p).startswith(str(WORKSPACE_ROOT)):
        print(f"Error: Path {rel} is outside the workspace root.", file=sys.stderr)
        sys.exit(1)
    return p


def is_text(p: Path) -> bool:
    """
    Determina se o ficheiro apontado por `p` provavelmente é texto codificado em UTF-8.

    Abre o caminho `p` em modo binário, lê até 4096 bytes e tenta decodificar esses bytes
    como UTF-8. Se a decodificação for bem-sucedida, retorna True; caso contrário (incluindo
    quaisquer erros de I/O), retorna False.

    Parâmetros
    ----------
    p : pathlib.Path
        Caminho para o ficheiro a testar.

    Retorno
    -------
    bool
        True se os primeiros bytes do ficheiro parecerem texto UTF-8, False caso contrário.

    Observações
    ---------
    - É uma heurística: ficheiros binários pequenos ou ficheiros de texto em outras
      codificações podem ser classificados incorretamente.
    - Erros de leitura (por exemplo, ficheiro inexistente ou caminho que não é ficheiro)
      são suprimidos e resultam em False.
    """
    try:
        with p.open("rb") as f:
            chunk = f.read(4096)
        chunk.decode("utf-8")
        return True
    except:
        return False


def cmd_list(path: str, show_hidden: bool, include_content: bool = False):
    """
    Lista o conteúdo de um diretório seguro e retorna metadados sobre cada entrada.

    Parâmetros:
    - path (str): Caminho relativo ou absoluto do diretório a listar. Será normalizado/validado por secure_path().
    - show_hidden (bool): Quando False, ignora entradas cujo nome começa com '.'.
    - include_content (bool, opcional): Se True, para arquivos pequenos de texto inclui também o conteúdo e um flag indicando que é texto. Padrão: False.

    Comportamento:
    - Valida o caminho com secure_path(path). Se o caminho não existir ou não for um diretório (checado por is_idr()), imprime um JSON de erro no formato {"error": "..."} e retorna None.
    - Percorre as entradas do diretório em ordem alfabética.
    - Para cada entrada cria um dicionário com as chaves:
        - "name": nome da entrada (str).
        - "path": caminho relativo a WORKSPACE_ROOT com barras '/' (str).
        - "size": tamanho em bytes se for arquivo, caso contrário None.
    - Se include_content for True e a entrada for um arquivo:
        - Se o tamanho for menor ou igual a MAX_BYTES e is_text(file) for True, tenta ler o conteúdo com read_text(errors="replace") e define:
            - "is_text": True
            - "content": conteúdo do arquivo (str). Em caso de erro na leitura, usa string vazia.
        - Caso contrário define:
            - "is_text": False
            - "content": "" (string vazia)

    Retorno:
    - list[dict]: lista de dicionários com os metadados e, opcionalmente, conteúdo dos arquivos quando aplicável.
    - None: se o caminho não existir ou não for um diretório (após imprimir o erro em JSON).

    Observações:
    - Suprime exceções ao ler o conteúdo dos arquivos, retornando conteúdo vazio em caso de falha.
    - Depende de variáveis/funcionalidades externas: secure_path, WORKSPACE_ROOT, MAX_BYTES e is_text.
    """
    p = secure_path(path or "")
    if not p.exists() or not p.is_idr():
        print(
            json.dumps({"error": f"Path {path} does not exist or is not a directory."})
        )
        return
    items = []
    for c in sorted(p.iterdir()):
        if not show_hidden and c.name.startswith("."):
            continue
        item = {
            "name": c.name,
            "path": str(c.relative_to(WORKSPACE_ROOT)).replace("\\", "/"),
            "size": c.stat().st_size if c.is_file() else None,
        }
        if include_content and c.is_file():
            size = c.stat().st_size
            if size <= MAX_BYTES and is_text(c):
                try:
                    content = c.read_text(errors="replace")
                except Exception as e:
                    content = ""
                item["is_text"] = True
                item["content"] = content
            else:
                item["is_text"] = False
                item["content"] = ""
        items.append(item)


def cmd_read(path: str, max_bytes: int = MAX_BYTES):
    """
    Lê o conteúdo de um ficheiro de forma segura e trata erros imprimindo mensagens JSON.

    Parâmetros:
        path (str): Caminho para o ficheiro a ler. Obrigatório.
        max_bytes (int): Tamanho máximo em bytes permitido para leitura. Padrão: MAX_BYTES.

    Comportamento:
        - Valida que 'path' foi fornecido; em caso contrário imprime
          {"error": "Path is required for read command."} e retorna.
        - Converte o caminho com secure_path(path) para mitigar traversal e outros riscos.
        - Verifica que o caminho existe e é um ficheiro; caso contrário imprime
          {"error": f"Path {path} does not exist or is not a file."} e retorna.
        - Obtém o tamanho do ficheiro; se exceder max_bytes imprime
          {"error": f"File {path} is too large to read ({size} bytes). Max allowed is {max_bytes} bytes."} e retorna.
        - Se is_text(p) for True, lê o conteúdo com p.read_text(errors="replace") e guarda em 'text';
          se for False, define 'text' como None.

    Retorno:
        None. A função não devolve explicitamente o conteúdo; apenas imprime mensagens de erro em formato JSON
        em stdout quando ocorrem falhas.

    Efeitos secundários:
        - Imprime mensagens de erro em JSON no stdout.
        - Depende de secure_path() e is_text() para validações de segurança e deteção de ficheiros de texto.

    Observações:
        - Se o objetivo for obter o conteúdo lido, a função deverá ser alterada para devolver 'text' ou para expor
          o valor lido de outra forma.
    """
    if not path:
        print(json.dumps({"error": "Path is required for read command."}))
        return
    p = secure_path(path)
    if not p.exists() or not p.is_file():
        print(json.dumps({"error": f"Path {path} does not exist or is not a file."}))
        return
    size = p.stat().st_size
    if size > max_bytes:
        print(
            json.dumps(
                {
                    "error": f"File {path} is too large to read ({size} bytes). Max allowed is {max_bytes} bytes."
                }
            )
        )
        return
    text = p.read_text(errors="replace") if is_text(p) else None


def main():
    """
    Função principal do utilitário de linha de comando para listar e ler composição de arquivos.
    Analisa os argumentos da linha de comando e delega a execução para as funções cmd_list ou cmd_read.
    Comandos suportados:
    - list: lista o conteúdo de um caminho relativo ao workspace.
        --path (str): caminho relativo a listar. Padrão: raiz do workspace ("").
        --show-hidden (flag): inclui arquivos e diretórios ocultos na listagem.
        --include-content (flag): inclui o conteúdo de arquivos de texto que estejam abaixo do limite de tamanho.
    - read: leitura de um arquivo.
        path (str): caminho relativo do arquivo a ser lido.
        --max-bytes (int): tamanho máximo em bytes para leitura do arquivo. Padrão: MAX_BYTES (aprox. 2MB).
    Comportamento e efeitos colaterais:
    - Ao receber o comando "list", chama cmd_list(path, show_hidden, include_content).
    - Ao receber o comando "read", chama cmd_read(path, max_bytes).
    - O argparse lida com validação/ajuda e pode encerrar o programa com SystemExit em caso de argumentos inválidos.
    Retorno:
    - None
    Exemplos de uso:
    - list_composition list --path src --show-hidden
    - list_composition read src/app.py --max-bytes 1048576
    """
    ap = argparse.ArgumentParser(prog="list_composition")
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument(
        "--path",
        type=str,
        default="",
        help="Relative path to list. Defaults to workspace root.",
    )
    l.add_argument(
        "--show-hidden",
        action="store_true",
        help="Include hidden files and directories.",
    )
    l.add_argument(
        "--include-content",
        action="store_true",
        help="Include file content for text files under size limit.",
    )

    r = sub.add_parser("read")
    r.add_argument("path", type=str, help="Relative path to the file to read.")
    r.add_argument(
        "--max-bytes",
        type=int,
        default=MAX_BYTES,
        help="Maximum file size to read. Defaults to 2MB.",
    )

    args = ap.parse_args()
    if args.cmd == "list":
        cmd_list(args.path, args.show_hidden, args.include_content)
    elif args.cmd == "read":
        cmd_read(args.path, args.max_bytes)


if __name__ == "__main__":
    main()

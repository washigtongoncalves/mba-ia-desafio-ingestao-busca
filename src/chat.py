import sys

from search import search_prompt


def main():
    print("Faca sua pergunta (linha em branco ou Ctrl+C para sair):")

    while True:
        try:
            pergunta = input("\nPERGUNTA: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not pergunta:
            break

        try:
            resposta = search_prompt(pergunta)
        except Exception as erro:
            print(f"Erro na busca: {erro}", file=sys.stderr)
            continue

        print(f"RESPOSTA: {resposta}")


if __name__ == "__main__":
    main()

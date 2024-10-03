import pandas as pd
from pathlib import Path
import sqlite3
import os
from datetime import datetime



print("***************************************************************")
print("Trabalho realizado pelos alunos Rafael Lucena da Costa e Pedro de Olivera Haro")
print("***************************************************************")



os.makedirs('data', exist_ok=True)


def criar_livro(titulo, autor, ano, preco):
    conn = sqlite3.connect('data/livraria.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER NOT NULL,
            preco INTEGER NOT NULL
        )
    ''')

    cursor.execute(
        "INSERT INTO livros (titulo, autor, ano, preco) VALUES (?,?,?,?)",
        (titulo, autor, ano, preco)
    )
    conn.commit()
    conn.close()

    print(f"Livro '{titulo}' criado com sucesso!")
    fazer_backup_banco_dados()


def listar_livros():
    conn = sqlite3.connect('data/livraria.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()

    conn.close()

    return livros


def excluir_livro(id_livro):
    conn = sqlite3.connect('data/livraria.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
    conn.commit()
    conn.close()

    print(f"Livro com id {id_livro} excluído com sucesso!")
    fazer_backup_banco_dados()


def editar_preco(id_livro):
    conn = sqlite3.connect('data/livraria.db')
    cursor = conn.cursor()

    preco_novo = float(input("Informe o novo preço: "))
    cursor.execute("UPDATE livros SET preco = ? WHERE id = ?", (preco_novo, id_livro))
    conn.commit()
    conn.close()

    print(f"Preço do livro com id {id_livro} alterado com sucesso!")
    fazer_backup_banco_dados()


def busca_por_autor(autor):
    conn = sqlite3.connect('data/livraria.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM livros WHERE autor = ?", (autor,))
    livros = cursor.fetchall()

    conn.close()

    return livros


def exportar_dados_csv():

    os.makedirs('exports', exist_ok=True)

    livros = listar_livros()
    df = pd.DataFrame(livros, columns=['id', 'titulo', 'autor', 'ano', 'preco'])
    df.to_csv('exports/livros-exportados.csv', index=False)

    print("Dados exportados para 'exports/livros-exportados.csv' com sucesso!")


def importar_dados_csv():
    csv_file = input("Digite o caminho completo do arquivo CSV (com extensão .csv): ")
    csv_path = Path(csv_file).resolve()

    print(f"Procurando o arquivo CSV em: {csv_path}")

    if csv_path.is_file():
        df = pd.read_csv(csv_path)
        conn = sqlite3.connect('data/livraria.db')
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO livros (titulo, autor, ano, preco) VALUES (?,?,?,?)",
                (row['titulo'], row['autor'], int(row['ano']), float(row['preco']))
            )

        conn.commit()
        conn.close()
        print(f"Dados importados de '{csv_file}' com sucesso!")
    else:
        print(f"Arquivo CSV '{csv_file}' não encontrado. Verifique se o arquivo existe e o caminho está correto.")


def fazer_backup_banco_dados():

    os.makedirs('backup', exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    backup_filename = f'backup/backup_livraria_{date_str}.db'

    with open('data/livraria.db', 'rb') as origem:
        with open(backup_filename, 'wb') as destino:
            destino.write(origem.read())

    print(f"Backup realizado com sucesso! Arquivo: {backup_filename}")



while True:
    print("\n*************** Sistema de Livraria ***************")
    print("1 - Adicionar Livro")
    print("2 - Listar Livros")
    print("3 - Excluir Livro")
    print("4 - Editar Preço")
    print("5 - Buscar Livros por Autor")
    print("6 - Exportar Dados para CSV")
    print("7 - Importar Dados de CSV")
    print("8 - Fazer Backup do Banco de Dados")
    print("9 - Sair")

    opcao = int(input("Escolha uma opção: "))


    if opcao == 1:
        titulo = input("Digite o título do livro: ")
        autor = input("Digite o autor do livro: ")
        ano = int(input("Digite o ano do livro: "))
        preco = float(input("Digite o preço do livro: "))
        criar_livro(titulo, autor, ano, preco)
    elif opcao == 2:
        livros = listar_livros()
        for livro in livros:
            print(livro)
    elif opcao == 3:
        id_livro = int(input("Digite o ID do livro a ser excluído: "))
        excluir_livro(id_livro)
    elif opcao == 4:
        id_livro = int(input("Digite o ID do livro a ter o preço editado: "))
        editar_preco(id_livro)
    elif opcao == 5:
        autor = input("Digite o autor dos livros a serem buscados: ")
        livros = busca_por_autor(autor)
        for livro in livros:
            print(livro)
    elif opcao == 6:
        exportar_dados_csv()
    elif opcao == 7:
        importar_dados_csv()
    elif opcao == 8:
        fazer_backup_banco_dados()
    elif opcao == 9:
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")
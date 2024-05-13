''''''

import oracledb
import pandas as pd
import requests


def main():
    conexao, inst_SQL, conn = conecta_BD()
    opc = 0
    while (opc != 9 and conexao == True):
        print("1-Cadastro dos Tutores")
        print("2-Cadastro dos Pets")
        print("3-Relatório de todos os pets de  determinado cliente")
        print("4-Relatório de todos os pets machos, cuja idade esteja entre 2 e 8 anos")
        print("5-Relatório de todos os pets cujo tutor resida na cidade de São Paulo, da raça Pug, cuja idade seja maior ou igual a 4 anos.")
        print("6-Exportar o relatório do item (3) para um arquivo texto")
        print("7-Exportar o relatório do item (4) para um arquivo texto")
        print("8-Exportar o relatório do item (5) para um arquivo texto")
        print("9-Sair")

        opc = int(input("Digite a opção (1-9): "))

        # Cadastro de Tutores
        if (opc == 1):
            opc_tutor = 0
            while (opc_tutor != 5):
                print("1-Inserção")
                print("2-Alteração")
                print("3-Exclusão")
                print("4-Exibição registros da tabela")
                print("5-Voltar")
                opc_tutor = int(input("Digite a opção (1-5): "))

                if (opc_tutor == 1):  # insert tutor
                    try:
                        tut_nome = input("Digite o nome do tutor: ")
                        tut_cpf = input("Digite cpf do tutor: ")
                        tut_telefone = input("Digite o telefone do tutor: ")
                        tut_idade = int(input("Digite a idade do tutor: "))
                        tut_CEP = input("Digite o CEP da residência (somente números): ")
                        url = f"""https://viacep.com.br/ws/{tut_CEP}/json/"""
                        requisicao = requests.get(url)
                        if (requisicao.status_code == 200):
                            dados_endereco = requisicao.json()
                            print(dados_endereco['logradouro'])
                            logradouro_nro = int(input("Digite o número: "))
                            tut_logradouro = dados_endereco['logradouro']
                            tut_bairro = dados_endereco['bairro']
                            tut_cidade = dados_endereco['localidade']
                        else:
                            print("CEP inexistente")

                        insercao = f"""INSERT INTO TUTOR (tut_nome,tut_cpf,tut_telefone,tut_cep,tut_logradouro,tut_numero,
                        tut_bairro,tut_cidade,tut_idade) 
                        VALUES ('{tut_nome}','{tut_cpf}','{tut_telefone}','{tut_CEP}','{tut_logradouro}',
                        {logradouro_nro},'{tut_bairro}','{tut_cidade}',{tut_idade})"""
                        insert_tabela(inst_SQL, conn, insercao)

                    except ValueError:
                        print("Digite dados numéricos")
                    except Exception as erro:
                        print("Erro: ", erro)
                elif (opc_tutor == 2):
                    lista_dados = []

                    id = int(input("Digite o id do tutor a ser alterado: "))

                    consulta = f"""SELECT * FROM tutor WHERE tut_id = {id}"""

                    inst_SQL.execute(consulta)
                    dados = inst_SQL.fetchall()

                    for dado in dados:
                        lista_dados.append(dado)

                    if (len(lista_dados) == 0):
                        print("Id não encontrado")
                    else:
                        try:
                            novo_nome = input("Digite o nome do tutor: ")
                            novo_cpf = input("Digite cpf do tutor: ")
                            novo_telefone = input("Digite o telefone do tutor: ")
                            nova_idade = int(input("Digite a idade do tutor: "))
                            novo_CEP = input("Digite o CEP da residência (somente números): ")
                            novo_CEP = novo_CEP.replace("-", "")
                            url = f"""https://viacep.com.br/ws/{novo_CEP}/json/"""
                            requisicao = requests.get(url)
                            if (requisicao.status_code == 200):
                                dados_endereco = requisicao.json()
                                print(dados_endereco['logradouro'])
                                logradouro_nro = int(input("Digite o número: "))
                                tutor_logradouro = dados_endereco['logradouro']
                                tutor_bairro = dados_endereco['bairro']
                                tutor_cidade = dados_endereco['localidade']
                            else:
                                print("CEP inexistente")

                        except ValueError:
                            print("Digite valores numéricos")
                        else:
                            str_update = f"""UPDATE tutor SET tut_nome='{novo_nome}',tut_cpf='{novo_cpf}',
                            tut_telefone='{novo_telefone}',tut_cep='{novo_CEP}',tut_logradouro='{tutor_logradouro}',
                            tut_numero={logradouro_nro},tut_bairro='{tutor_bairro}',tut_cidade='{tutor_cidade}',
                            tut_idade={nova_idade} WHERE tut_id={id}"""
                            update_tabela(inst_SQL, conn, str_update)
                elif (opc_tutor == 3):
                    lista_dados = []

                    id = int(input("Digite o Id do tutor a ser excluído: "))

                    consulta = f"""SELECT * FROM tutor WHERE tut_id = {id}"""

                    inst_SQL.execute(consulta)
                    dados = inst_SQL.fetchall()

                    for dado in dados:
                        lista_dados.append(dado)

                    if (len(lista_dados) == 0):
                        print("O id digitado não existe na tabela")
                    else:
                        # Excluir os pets associados ao tutor
                        str_delete_pets = f"""DELETE FROM pet WHERE tut_id={id}"""
                        delete_tabela(inst_SQL, conn, str_delete_pets)

                        # Excluir o tutor
                        str_delete_tutor = f"""DELETE FROM tutor WHERE tut_id={id}"""
                        delete_tabela(inst_SQL, conn, str_delete_tutor)
                elif (opc_tutor == 4):
                    str_consulta = 'SELECT t.tut_id,t.tut_nome,t.tut_cpf,t.tut_telefone,t.tut_cep,t.tut_logradouro,t.tut_numero,t.tut_bairro,t.tut_cidade,t.tut_idade FROM tutor t'
                    colunas = ['ID', 'NOME', 'CPF', 'TELEFONE', 'CEP', 'LOGRADOURO', 'NUMERO', 'BAIRRO', 'CIDADE',
                               'IDADE']
                    consulta_tabela(inst_SQL, str_consulta, colunas, False)

        elif (opc == 2):
            opc_pet = 0
            while (opc_pet != 5):
                print("1-Inserção")
                print("2-Alteração")
                print("3-Exclusão")
                print("4-Exibição registros da tabela")
                print("5-Voltar")
                opc_pet = int(input("Digite a opção (1-5): "))

                if (opc_pet == 1):  # inserção pet
                    try:
                        nome = input('Digite o nome do pet: ')
                        raca = input("Digite a raça do pet: ")
                        porte = input("Digite o porte do pet: ")
                        idade = int(input("Digite a idade do pet: "))
                        sexo = input("Digite o sexo (M - macho / F - fêmea): ")
                        str_consulta = 'SELECT * FROM tutor'
                        str_colunas = f"""SELECT column_name FROM all_tab_cols WHERE table_name = 'TUTOR' AND OWNER = 'RM553801'"""
                        inst_SQL.execute(str_colunas)
                        dados = inst_SQL.fetchall()
                        colunas = []
                        for i in range(len(dados)):
                            colunas.append(dados[i][0].split("_")[1])

                        consulta_tabela(inst_SQL, str_consulta, colunas, False)

                        lista_dados = []

                        id_tutor = int(input("Digite o id do tutor a ser vinculado ao pet: "))

                        consulta = f"""SELECT * FROM tutor WHERE tut_id = {id_tutor}"""

                        inst_SQL.execute(consulta)
                        dados = inst_SQL.fetchall()

                        for dado in dados:
                            lista_dados.append(dado)

                        if (len(lista_dados) == 0):
                            print("Id não encontrado")
                    except ValueError:
                        print("Digite valores numéricos")
                    else:
                        insercao = f"""INSERT INTO PET (pet_nome,pet_raca,pet_porte,pet_idade,pet_sexo,tut_id) 
                        VALUES ('{nome}','{raca}','{porte}',{idade},'{sexo}',{id_tutor})"""
                        insert_tabela(inst_SQL, conn, insercao)
                elif (opc_pet == 2):  # alteração pet
                    lista_dados = []

                    id_pet = int(input("Digite o id do pet a ser alterado: "))

                    consulta = f"""SELECT * FROM pet WHERE pet_id = {id_pet}"""

                    inst_SQL.execute(consulta)
                    dados = inst_SQL.fetchall()

                    for dado in dados:
                        lista_dados.append(dado)

                    if (len(lista_dados) == 0):
                        print("Id não encontrado")
                    else:
                        try:
                            novo_nome_pet = input("Digite o novo nome do pet: ")
                            nova_raca_pet = input("Digite a raça do pet: ")
                            novo_porte_pet = input("Digite o porte do pet: ")
                            nova_idade_pet = int(input("Digite a idade do pet: "))
                            novo_sexo_pet = input("Digite o sexo (M - macho / F - fêmea): ")
                            str_consulta = 'SELECT * FROM tutor'
                            str_colunas = f"""SELECT column_name FROM all_tab_cols WHERE table_name = 'TUTOR' AND OWNER = 'RM553801'"""
                            inst_SQL.execute(str_colunas)
                            dados = inst_SQL.fetchall()
                            colunas = []
                            for i in range(len(dados)):
                                colunas.append(dados[i][0].split("_")[1])

                            consulta_tabela(inst_SQL, str_consulta, colunas, False)

                            lista_dados = []

                            id_tutor_pet = int(input("Digite o id do novo tutor a ser vinculado ao pet: "))

                            consulta = f"""SELECT * FROM tutor WHERE tut_id = {id_tutor_pet}"""

                            inst_SQL.execute(consulta)
                            dados = inst_SQL.fetchall()

                            for dado in dados:
                                lista_dados.append(dado)

                            if (len(lista_dados) == 0):
                                print("Id não encontrado")
                        except ValueError:
                            print("Digite valores numéricos")
                        else:
                            str_update = f"""UPDATE pet SET pet_nome='{novo_nome_pet}',pet_raca='{nova_raca_pet}',pet_porte='{novo_porte_pet}',pet_idade={nova_idade_pet},pet_sexo='{novo_sexo_pet}',tut_id={id_tutor_pet} WHERE pet_id={id_pet}"""
                            update_tabela(inst_SQL, conn, str_update)
                elif (opc_pet == 3):
                    lista_dados = []

                    id_pet = int(input("Digite o Id do pet a ser excluído: "))

                    consulta = f"""SELECT * FROM pet WHERE pet_id = {id_pet}"""

                    inst_SQL.execute(consulta)
                    dados = inst_SQL.fetchall()

                    for dado in dados:
                        lista_dados.append(dado)

                    if (len(lista_dados) == 0):
                        print("O id digitado não existe na tabela")
                    else:
                        str_delete = f"""DELETE FROM pet WHERE pet_id={id_pet}"""
                        delete_tabela(inst_SQL, conn, str_delete)
                elif (opc_pet == 4):
                    str_consulta = 'SELECT p.pet_id,p.pet_nome,p.pet_raca,p.pet_porte,p.pet_idade,p.pet_sexo,p.Tut_id FROM pet p'
                    colunas = ['ID', 'NOME', 'RACA', 'PORTE', 'IDADE', 'SEXO', 'ID_CLIENTE']
                    consulta_tabela(inst_SQL, str_consulta, colunas, False)

        elif (opc == 3):
            id_tutor = int(input("Digite o ID do tutor: "))
            str_relatorio = f"""
                SELECT p.pet_id, p.pet_nome, p.pet_raca, p.pet_porte, p.pet_idade, p.pet_sexo
                FROM pet p
                INNER JOIN tutor t ON p.id_cliente = t.tutor_id
                WHERE t.tutor_id = {id_tutor}
            """
            colunas = ['ID', 'NOME', 'RACA', 'PORTE', 'IDADE', 'SEXO']
            gerar_relatorio(inst_SQL, str_relatorio, colunas, False)

        elif (opc == 4):
            str_relatorio = f"""
                SELECT p.pet_id, p.pet_nome, p.pet_raca, p.pet_porte, p.pet_idade, p.pet_sexo
                FROM pet p
                WHERE p.pet_sexo = 'M' AND p.pet_idade BETWEEN 2 AND 8
            """
            colunas = ['ID', 'NOME', 'RACA', 'PORTE', 'IDADE', 'SEXO']
            gerar_relatorio(inst_SQL, str_relatorio, colunas, False)

        elif (opc == 5):
            str_relatorio = f"""
                SELECT p.pet_id, p.pet_nome, p.pet_raca, p.pet_porte, p.pet_idade, p.pet_sexo
                FROM pet p
                INNER JOIN tutor t ON p.tut_id = t.tut_id
                WHERE t.tut_cidade = 'São Paulo' AND p.pet_raca = 'Pug' AND p.pet_idade >= 4
            """
            colunas = ['ID', 'NOME', 'RACA', 'PORTE', 'IDADE', 'SEXO']
            gerar_relatorio(inst_SQL, str_relatorio, colunas, False)

        elif (opc == 6):
            id_tutor = int(input("Digite o ID do tutor: "))
            str_relatorio = f"""
                SELECT p.pet_id, p.pet_nome, p.pet_raca, p.pet_porte, p.pet_idade, p.pet_sexo
                FROM pet p
                INNER JOIN tutor t ON p.Tut_id = t.tut_id
                WHERE t.tut_id = {id_tutor}
            """
            colunas = ['ID', 'NOME', 'RACA', 'PORTE', 'IDADE', 'SEXO']
            gerar_relatorio(inst_SQL, str_relatorio, colunas, True)

        elif (opc == 7):
            str_relatorio = f"""
                SELECT p.pet_id, p.pet_nome, p.pet_raca, p.pet_porte, p.pet_idade, p.pet_sexo
                FROM pet p
                WHERE p.pet_sexo = 'M' AND p.pet_idade BETWEEN 2 AND 8
            """
            colunas = ['ID', 'NOME', 'RACA', 'PORTE', 'IDADE', 'SEXO']
            gerar_relatorio(inst_SQL, str_relatorio, colunas, True)

        elif (opc == 8):
            str_relatorio = f"""
                SELECT p.pet_id, p.pet_nome, p.pet_raca, p.pet_porte, p.pet_idade, p.pet_sexo
                FROM pet p
                INNER JOIN tutor t ON p.Tut_id = t.tut_id
                WHERE t.tut_cidade = 'São Paulo' AND p.pet_raca = 'Pug' AND p.pet_idade >= 4
            """
            colunas = ['ID', 'NOME', 'RACA', 'PORTE', 'IDADE', 'SEXO']
            gerar_relatorio(inst_SQL, str_relatorio, colunas, True)


'''CONEXÃO BANCO DE DADOS'''


def conecta_BD():
    try:
        # Conectar com o Servidor
        dnStr = oracledb.makedsn("oracle.fiap.com.br", "1521", "ORCL")
        # Efetuar a conexão com o usuário
        conn = oracledb.connect(user='RM553801', password='301003', dsn=dnStr)

        # Criar as instruções para cada módulo
        inst_SQL = conn.cursor()

    except Exception as e:
        print("Erro: ", e)
        conexao = False
        inst_SQL = ""
        conn = ""
    else:
        conexao = True

    return (conexao, inst_SQL, conn)


'''INSERÇÃO DE DADOS'''


def insert_tabela(inst_SQL, conn, insercao):
    try:
        inst_SQL.execute(insercao)
        conn.commit()
    except:
        print("Erro de transação com o BD")
    else:
        print("Dados gravados com sucesso")


'''CONSULTA A TABELA'''


def consulta_tabela(inst_SQL, str_consulta, colunas, gera_txt):
    lista = []

    # Executa a consulta (Select) no BD
    inst_SQL.execute(str_consulta)

    # Captura todos os registros vindos pela consulta
    dados = inst_SQL.fetchall()

    # Insere os registros em uma lista
    for registro in dados:
        lista.append(registro)

    # Ordena a lista
    lista = sorted(lista)

    # Gera um Dataframe com os dados da lista (Pandas)
    base_df = pd.DataFrame.from_records(lista, columns=colunas, index=colunas[0])

    if (base_df.empty):
        print("Não há registros cadastrados")
    else:
        if (gera_txt):
            texto = base_df.to_string()
            nome_arq = input("Digite o nome do arquivo texto a ser gerado: ")
            with open(nome_arq, "w", encoding="utf-8") as arq:
                arq.write(texto)
            print("Arquivo gerado com sucesso!")
        else:
            print(base_df)
        print("\n")


'''ATUALIZA DADOS DA TABELA'''


def update_tabela(inst_SQL, conn, str_update):
    try:
        inst_SQL.execute(str_update)
        conn.commit()
    except Exception as e:
        print("Erro de transação com o BD: ", str(e))
    else:
        print("Dados alterados com sucesso")


'''DELETA A TABELA'''


def delete_tabela(inst_SQL, conn, str_delete):
    try:
        inst_SQL.execute(str_delete)
        conn.commit()
    except:
        print("Erro de transação com o BD")
    else:
        print("Dados excluídos com sucesso")


def gerar_relatorio(inst_SQL, str_relatorio, colunas, gera_txt):
    lista_dados = []

    inst_SQL.execute(str_relatorio)
    dados = inst_SQL.fetchall()

    for dado in dados:
        lista_dados.append(dado)

    lista_dados = sorted(lista_dados)

    base_df = pd.DataFrame.from_records(lista_dados, columns=colunas, index=colunas[0])

    if (base_df.empty):
        print("Não há registros na tabela")
    else:
        if (gera_txt):
            texto = base_df.to_string()
            nome_arq = input("Digite o nome do arquivo texto a ser gerado: ")
            with open(nome_arq, "w", encoding="utf-8") as arq:
                arq.write(texto)
            print("Arquivo gerado com sucesso!")
        else:
            print(base_df)
        print("\n")


if (__name__ == "__main__"):
    main()


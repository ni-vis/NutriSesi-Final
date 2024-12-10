from flask import Flask, render_template, request, redirect, session
import mysql.connector
from mysql.connector import Error
import pdfkit
import uuid
from config import *
from db_functions import *
from datetime import datetime
from flask import flash, redirect
from datetime import date
app = Flask(__name__)
app.secret_key = SECRET_KEY

# FUNÇÃO PARA VERIFICAR SESSÃO
def verifica_sessao():
    return "login" in session and session["login"]

# ROTA DA PÁGINA INICIAL
@app.route("/")
def index():
    if session:
        return redirect ("/adm")
    else:
        return render_template("home.html")

# ROTA DA PÁGINA ACESSO
@app.route("/login", methods=['POST','GET'])
def acesso():
    if request.method == 'GET':
        return redirect ("/")
    
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]

    if usuario_informado == ADM_USER  and senha_informada == ADM_PASSWORD:
        session["adm"] = True
        return redirect('/adm')
    else:
        return render_template("home.html", msg="Usuário/Senha estão incorretos!")


# ROTA DA PÁGINA ADM - VER CARDAPIOS 
@app.route("/adm")
def adm():
    if not session:
        return redirect("/")
    
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = """
        SELECT DISTINCT c.idCardapio, c.data, cat.Nome
        FROM Cardapio c
        JOIN Feedback f ON c.idCardapio = f.idCardapio
        JOIN Categoria cat ON c.idCategoria = cat.idCategoria
        ORDER BY c.data DESC;
        """
        # tabela cardapio
        cursor.execute(comandoSQL)
        cardapios = cursor.fetchall()
        # Formatar a data no padrão dd/mm/yyyy
        cardapios_formatados = []
        if cardapios:
            for cardapio in cardapios:
                id_cardapio = cardapio[0]
                # Se cardapio[1] já é um objeto datetime.date, use strftime() diretamente
                data_cardapio = cardapio[1].strftime('%d/%m/%Y')
                cat_cardapio = cardapio[2]
                # Adiciona o cardápio formatado na lista
                cardapios_formatados.append((id_cardapio, data_cardapio, cat_cardapio))
       
        return render_template("adm.html", cardapios=cardapios_formatados)
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/adm")
    except Exception as e:
        print(f"Erro: {e}")
        return redirect("/adm")
    finally: 
        encerrar_db(cursor, conexao)

# CÓDIGO DO LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/bebida")
def bebidas():
    if not session:
        return redirect("/")
    
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'SELECT * FROM Bebida'
        # tabela cardapio
        cursor.execute(comandoSQL)
        bebidas = cursor.fetchall()    
        return render_template("bebidas.html", bebidas=bebidas)
    except:
        print("banco de dados com problema!")
    finally: 
        encerrar_db(cursor, conexao)
        
@app.route("/cadbebidas", methods=['POST','GET'])
def cadbebidas():
    if not session:
        return redirect("/")
    
    if request.method == 'GET':
        return redirect("/")
    
    bebida = request.form["nome_bebida"]

    if not bebida:
        return redirect ("/bebida")
    
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'INSERT INTO Bebida (Nome) VALUES (%s);'

        # tabela cardapio
        cursor.execute(comandoSQL, (bebida,))
        conexao.commit() 
        return redirect ("/bebida")
    except:
        print("banco de dados com problema!")
        return redirect ("/bebida")
    finally: 
        encerrar_db(cursor, conexao)

from mysql.connector import Error

# Rota para excluir um item de qualquer tipo
@app.route("/excluir/<tipo>/<int:id>")
def excluir_item(tipo, id):
    if not session:
        return redirect("/")

    conexao, cursor = iniciar_db()

    try:
        # Verificar se o tipo é válido
        if tipo in ['bebida','sobremesa','salada','prato_principal']:
            # Executar a exclusão do item com o ID especificado
            cursor.execute(f'DELETE FROM {tipo} WHERE id{tipo} = %s', (id,))
            conexao.commit()
            print(f"{tipo.capitalize()} com id {id} excluído com sucesso.")
            return redirect(f"/{tipo}")
        else:
            print("Tipo inválido para exclusão.")
    except Error as e:
        if e.errno == 1451:
            if tipo == "bebida":
                return render_template ("bebidas.html", erro = "Você não pode excluir esse item!")
            elif tipo == "sobremesa":
                return render_template ("sobremesas.html", erro = "Você não pode excluir esse item!")
            elif tipo == "salada":
                return render_template ("saladas.html", erro = "Você não pode excluir esse item!")
            elif tipo == "prato_principal":
                return render_template ("pratosprincipais.html", erro = "Você não pode excluir esse item!")
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        encerrar_db(cursor, conexao)


@app.route("/editar_bebida/<int:id>/<bebida>")
def editar_bebida(id, bebida):
    if not session:
        return redirect("/")
    
    try:
        if not bebida or not id:
            return redirect("/bebida")
        
        conexao, cursor = iniciar_db()
        cursor.execute('UPDATE Bebida SET Nome = %s WHERE idBebida = %s', (bebida, id))
        conexao.commit()
        return redirect("/bebida")
    except Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/adm")

    finally:
        encerrar_db(cursor, conexao)


#----------------SALADA-------------------------
@app.route("/salada")
def saladas():
    if not session:
        return redirect("/")
    
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'SELECT * FROM salada'
        # tabela cardapio
        cursor.execute(comandoSQL)
        saladas = cursor.fetchall()    
        return render_template("saladas.html", saladas=saladas)
    except:
        print("banco de dados com problema!")
    finally: 
        encerrar_db(cursor, conexao)
        
@app.route("/cadsaladas", methods=['POST','GET'])
def cadsaladas():
    if not session:
        return redirect("/")
    
    if request.method == 'GET':
        return redirect("/")
    
    salada = request.form["nome_salada"]

    if not salada:
        return redirect ("/salada")
    
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'INSERT INTO Salada (Nome) VALUES (%s);'

        # tabela cardapio
        cursor.execute(comandoSQL, (salada,))
        conexao.commit() 
        return redirect ("/salada")
    except:
        print("banco de dados com problema!")
        return redirect ("/salada")
    finally: 
        encerrar_db(cursor, conexao)

@app.route("/editar_salada/<int:id>/<salada>")
def editar_salada(id, salada):
    if not session:
        return redirect("/")
    
    try:
        if not salada or not id:
            return redirect("/salada")
        
        conexao, cursor = iniciar_db()
        cursor.execute('UPDATE Salada SET Nome = %s WHERE idSalada = %s', (salada, id))
        conexao.commit()
        return redirect("/salada")
    except Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/adm")
    finally:
        encerrar_db(cursor, conexao)


#----------------SOBREMESA-------------------------
@app.route("/sobremesa")
def sobremesas():
    if not session:
        return redirect("/")  
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'SELECT * FROM sobremesa'
        # tabela cardapio
        cursor.execute(comandoSQL)
        sobremesas = cursor.fetchall()    
        return render_template("sobremesas.html", sobremesas=sobremesas)
    except:
        print("banco de dados com problema!")
    finally: 
        encerrar_db(cursor, conexao)
        
@app.route("/cadsobremesas", methods=['POST','GET'])
def cadsobremesas():
    if not session:
        return redirect("/")  
    
    if request.method == 'GET':
        return redirect("/")
    sobremesa = request.form["nome_sobremesa"]

    if not sobremesa:
        return redirect ("/sobremesa")
    
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'INSERT INTO Sobremesa (Nome) VALUES (%s);'

        # tabela cardapio
        cursor.execute(comandoSQL, (sobremesa,))
        conexao.commit() 
        return redirect ("/sobremesa")
    except:
        print("banco de dados com problema!")
        return redirect ("/sobremesa")
    finally: 
        encerrar_db(cursor, conexao)

@app.route("/editar_sobremesa/<int:id>/<sobremesa>")
def editar_sobremesa(id, sobremesa):
    if not session:
        return redirect("/")
    
    try:
        if not sobremesa or not id:
            return redirect("/sobremesa")
        
        conexao, cursor = iniciar_db()
        cursor.execute('UPDATE Sobremesa SET Nome = %s WHERE idSobremesa = %s', (sobremesa, id))
        conexao.commit()
        return redirect("/sobremesa")
    except Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/adm")
    finally:
        encerrar_db(cursor, conexao)


#----------------PRATO PRINCIPAL-------------------------
@app.route("/prato_principal")
def pratosprincipais():
    if not session:
        return redirect("/")
    
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'SELECT * FROM Prato_principal'
        # tabela cardapio
        cursor.execute(comandoSQL)
        pratosprincipais = cursor.fetchall()    
        return render_template("pratosprincipais.html", pratosprincipais=pratosprincipais)
    except:
        print("banco de dados com problema!")
    finally: 
        encerrar_db(cursor, conexao)
        
@app.route("/cadpratosprincipais", methods=['POST','GET'])
def cadpratosprincipais():
    if not session:
        return redirect("/")
    
    if request.method == 'GET':
        return redirect("/")
    
    pratoprincipal = request.form["nome_pratoprincipal"]

    if not pratoprincipal:
        return redirect ("/prato_principal")
    
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'INSERT INTO prato_principal (Nome) VALUES (%s);'

        # tabela cardapio
        cursor.execute(comandoSQL, (pratoprincipal,))
        conexao.commit() 
        return redirect ("/prato_principal")
    except:
        print("banco de dados com problema!")
        return redirect ("/prato_principal")
    finally: 
        encerrar_db(cursor, conexao)

@app.route("/editar_prato/<int:id>/<prato>")
def editar_prato(id, prato):
    if not session:
        return redirect("/")
    
    try:
        if not prato or not id:
            return redirect("/prato_principal")
        
        conexao, cursor = iniciar_db()
        cursor.execute('UPDATE Prato_principal SET Nome = %s WHERE idPrato_principal = %s', (prato, id))
        conexao.commit()
        return redirect("/prato_principal")
    except Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/adm")
    finally:
        encerrar_db(cursor, conexao)

#-----------CARDÁPIOS-----------
@app.route("/cardapios", methods=['GET', 'POST'])
def criar_cardapio():
    if not session:
        return redirect("/")

    if request.method == 'GET':
        try:
            # Carregar todas as opções
            conexao, cursor = iniciar_db()

            cursor.execute('SELECT * FROM Bebida')
            bebidas = cursor.fetchall()
            
            cursor.execute('SELECT * FROM Sobremesa')
            sobremesas = cursor.fetchall()
            
            cursor.execute('SELECT * FROM Prato_principal')
            pratosprincipais = cursor.fetchall()
            
            cursor.execute('SELECT * FROM Salada')
            saladas = cursor.fetchall()

            cursor.execute('SELECT * FROM Categoria')
            categorias = cursor.fetchall()

            comandoSQL = """ 
            SELECT cardapio.data, b.nome, sb.nome, p.nome, s.nome, c.nome, cardapio.idCardapio
            FROM cardapio
            LEFT JOIN bebida b ON b.idBebida = cardapio.idBebida
            JOIN sobremesa sb ON sb.idSobremesa = cardapio.idSobremesa
            JOIN prato_principal p ON p.idPrato_principal = cardapio.idPrato_principal
            LEFT JOIN salada s ON s.idSalada = cardapio.idSalada
            JOIN categoria c ON c.idCategoria = cardapio.idCategoria
            ORDER BY cardapio.data DESC
            """
            cursor.execute(comandoSQL)
            cardapios = cursor.fetchall()

            return render_template(
                "cadcardapios.html", 
                bebidas=bebidas, 
                sobremesas=sobremesas, 
                pratosprincipais=pratosprincipais, 
                saladas=saladas, 
                categorias=categorias,
                cardapios=cardapios
            )
        except Exception as e:
            print(f"Erro ao carregar opções: {e}")
            return redirect("/")
        finally:
            encerrar_db(cursor, conexao)

    if request.method == "POST":
        data = request.form.get("data")
        pratoprincipal = request.form.get("pratoprincipal")
        sobremesa = request.form.get("sobremesa")
        categoria = request.form.get("categoria")
        bebida = request.form.get("bebida") or None
        salada = request.form.get("salada") or None

        # Verificar se todos os campos obrigatórios estão preenchidos
        if not data or not pratoprincipal or not categoria or not sobremesa:
            print("Erro: Campos obrigatórios faltando.")
            return redirect("/adm")

        try:
            conexao, cursor = iniciar_db()
            print(f"Tentando inserir cardápio: data={data}, bebida={bebida}, sobremesa={sobremesa}, prato principal={pratoprincipal}, salada={salada}, categoria={categoria}")

            if categoria == "1" or categoria == "3":
                comandoSQL = '''
                INSERT INTO cardapio (data, idBebida, idSobremesa, idPrato_principal, idCategoria)
                VALUES (%s, %s, %s, %s, %s);
                '''
                cursor.execute(comandoSQL, (data, bebida, sobremesa, pratoprincipal, categoria))
            else:
                comandoSQL = '''
                INSERT INTO cardapio (data, idSobremesa, idPrato_principal, idSalada, idCategoria)
                VALUES (%s, %s, %s, %s, %s);
                '''
                cursor.execute(comandoSQL, (data, sobremesa, pratoprincipal, salada, categoria))

            conexao.commit()
            print("Cardápio inserido com sucesso.")
            return redirect("/cardapios")

        except Exception as e:
            print(f"Erro ao cadastrar cardápio: {e}")
            return redirect("/erro")
        finally:
            encerrar_db(cursor, conexao)


# VER UM CARDÁPIO INDIVIDUAL
@app.route("/vercardapio/<int:idCardapio>", methods=['GET'])
def ver_cardapio_individual(idCardapio):
    if not session:
        return redirect("/")

    try:
        # Conectar ao banco de dados
        conexao, cursor = iniciar_db()

        # Consulta SQL para buscar detalhes de um cardápio específico
        comandoSQL = """ 
        SELECT cardapio.data, b.nome AS bebida, sb.nome AS sobremesa, p.nome AS prato_principal, 
               s.nome AS salada, c.nome AS categoria, cardapio.idCardapio
        FROM cardapio
        LEFT JOIN bebida b ON b.idBebida = cardapio.idBebida
        JOIN sobremesa sb ON sb.idSobremesa = cardapio.idSobremesa
        JOIN prato_principal p ON p.idPrato_principal = cardapio.idPrato_principal
        LEFT JOIN salada s ON s.idSalada = cardapio.idSalada
        JOIN categoria c ON c.idCategoria = cardapio.idCategoria
        WHERE cardapio.idCardapio = %s
        """
        cursor.execute(comandoSQL, (idCardapio,))
        cardapio = cursor.fetchone()

        if not cardapio:
            return "Cardápio não encontrado", 404

        # Renderizar o template com os detalhes do cardápio
        return render_template(
            "vercardapios.html",
            cardapio=cardapio
        )
    except Exception as e:
        print(f"Erro: {e}")
        return redirect("/")
    finally:
        encerrar_db(cursor, conexao)


#CRIAR A ROTA PARA TRATAR A EDIÇÃO
@app.route("/editarcardapios/<int:id_cardapio>", methods=['GET','POST'])
def editcardapio(id_cardapio):
    if not session:
        return redirect("/")


    if request.method == 'GET':

        try:
            # Carregar todas as opções
            conexao, cursor = iniciar_db()

            cursor.execute('SELECT * FROM Bebida')
            bebidas = cursor.fetchall()
            
            cursor.execute('SELECT * FROM Sobremesa')
            sobremesas = cursor.fetchall()
            
            cursor.execute('SELECT * FROM prato_principal')
            pratosprincipais = cursor.fetchall()
            
            cursor.execute('SELECT * FROM Salada')
            saladas = cursor.fetchall()

            cursor.execute('SELECT * FROM Categoria')
            categorias = cursor.fetchall()

            comandoSQL= """ 
            SELECT * FROM cardapio WHERE idCardapio = %s
            """
            cursor.execute(comandoSQL, (id_cardapio,))
            cardapio = cursor.fetchone()
     
            return render_template(
                "editcardapios.html", 
                bebidas=bebidas, 
                sobremesas=sobremesas, 
                pratosprincipais=pratosprincipais, 
                saladas=saladas, 
                categorias=categorias,
                cardapio=cardapio
            )
        except Exception as e:
            print(f"Erro: {e}")
            return redirect("/")
        finally:
            encerrar_db(cursor, conexao) 

    if request.method == "POST":
        data = request.form["data"]
        pratoprincipal = request.form["pratoprincipal"]
        sobremesa = request.form["sobremesa"]
        categoria = request.form["categoria"]
        bebida = request.form.get("bebida") or None
        salada = request.form.get("salada") or None
      
        if not data or not pratoprincipal or not categoria or not sobremesa:
            return redirect("/adm")

        try:
            conexao, cursor = iniciar_db()
            if categoria == "1" or categoria == "3":
                comandoSQL = 'UPDATE cardapio SET data= %s,idBebida = %s, idSobremesa= %s,  idPrato_principal= %s WHERE idCardapio = %s'
                cursor.execute(comandoSQL, (data, bebida, sobremesa, pratoprincipal, id_cardapio))  
            else:
                comandoSQL = 'UPDATE cardapio SET data= %s,idSobremesa= %s, idPrato_principal= %s, idSalada= %s WHERE idCardapio = %s'
                cursor.execute(comandoSQL, (data, sobremesa, pratoprincipal, salada, id_cardapio)) 

            conexao.commit() 
            return redirect("/cardapios")
        except mysql.connector.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return redirect("/adm")
        except Exception as e:
            print(f"Erro: {e}")
            return redirect("/adm")
        finally: 
            encerrar_db(cursor, conexao)

@app.route("/cardapios/excluir/<int:id>")
def excluir_cardapio(id):
    if not session:
        return redirect("/")

    conexao, cursor = iniciar_db()

    try:
        # Executar a exclusão do item com o ID especificado
        cursor.execute('DELETE FROM feedback WHERE idCardapio = %s', (id,))
        conexao.commit()
        # Executar a exclusão do item com o ID especificado
        cursor.execute('DELETE FROM cardapio WHERE idCardapio = %s', (id,))
        conexao.commit()

        print(f"Cardápio com id {id} excluído com sucesso.")
        return redirect("/cardapios")
    except Error as e:
        print(e)
        if e.errno == 1451:
            flash("Você não pode excluir este item porque ele está vinculado a um feedback ou outro registro.", "erro")
            return redirect("/cardapios")
    finally:
        encerrar_db(cursor, conexao)

#----------------- ROTA FEEDBACK -----------------
@app.route("/feedback")
def feedback():
    if not session:
        return redirect("/")
        
    try:
        conexao, cursor = iniciar_db()
        # Obter a data atual no formato YYYY-MM-DD
        data_atual = date.today().isoformat()

        # Selecionar todos os cardápios com base na data atual
        consulta = "SELECT * FROM Cardapio WHERE data = %s ORDER BY data DESC"
        cursor.execute(consulta, (data_atual,))
        cardapios = cursor.fetchall()

        return render_template("Feedback.html", cardapios=cardapios)
    
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/adm")
    
    finally:
        encerrar_db(cursor, conexao)

@app.route("/votacao/<int:idCardapio>")
def votacao(idCardapio):
    if not session:
        return redirect("/")
    
    session['idcardapio'] = idCardapio  # Garantir que o ID do cardápio seja atribuído à sessão
    return render_template('votacao.html')

@app.route("/esperavotacao")
def espera_votacao():
    if 'idcardapio' not in session:
        flash("Erro: Nenhum cardápio selecionado para votação.", "erro")
        return redirect("/vercardapios")
    
    return render_template('votacao.html')
 

# ROTA DE INICIAR VOTAÇÃO
@app.route("/iniciarvotacao")
def iniciar_votacao():
    if request.method == 'GET':
        return render_template('votacao_cardapio.html')
    
# ROTA DE INICIAR VOTAÇÃO
@app.route("/aprovacao/<int:idCardapio>")
def aprovacao(idCardapio):
    try:
        conexao, cursor = iniciar_db()
        comandoSQL = 'INSERT INTO feedback (aprovacao, comentario, idCardapio) VALUES (1,"Cardápio aprovado com sucesso", %s)'
        cursor.execute(comandoSQL, (idCardapio,))  
        conexao.commit() 
        return render_template("concluido.html")
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/feedback")
    except Exception as e:
        print(f"Erro: {e}")
        return redirect("/feedback")
    finally: 
        encerrar_db(cursor, conexao)

# ROTA DE INICIAR VOTAÇÃO
@app.route("/reprovacao/<int:idCardapio>")
def reprovacao(idCardapio):
    try:
        conexao, cursor = iniciar_db()
        comandoSQL= """ 
            SELECT b.nome, sb.nome, p.nome, s.nome, c.nome, cardapio.idCardapio
            FROM cardapio
            LEFT JOIN bebida b ON b.idBebida = cardapio.idBebida
            JOIN sobremesa sb ON sb.idSobremesa = cardapio.idSobremesa
            JOIN prato_principal p ON p.idPrato_principal = cardapio.idPrato_principal
            LEFT JOIN salada s ON s.idSalada = cardapio.idSalada
            JOIN categoria c ON c.idCategoria = cardapio.idCategoria
            WHERE cardapio.idCardapio = %s
            """
        cursor.execute(comandoSQL, (idCardapio,))  
        cardapio=cursor.fetchone()
        session['idCardapio'] = idCardapio
        return render_template("reprovacao.html",cardapio=cardapio)
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/feedback")
    except Exception as e:
        print(f"Erro: {e}")
        return redirect("/feedback")
    finally: 
        encerrar_db(cursor, conexao)


# ROTA DE INICIAR VOTAÇÃO
@app.route("/salvar_reprovacao", methods=['POST'])
def salvar_reprovacao():
    if request.method == "POST":
        data = request.get_json()

        # Captura os comentários
        pratoprincipal = data.get("comments_prato")
        bebida = data.get("comments_bebida")
        sobremesa = data.get("comments_sobremesa")
        salada = data.get("comments_salada")

        # Validação de entrada
        comentario = ""
        if pratoprincipal:
            comentario += f"Prato principal: {pratoprincipal}"
        if bebida:
            comentario += f" - Bebida: {bebida}"
        if sobremesa:
            comentario += f" - Sobremesa: {sobremesa}"
        if salada:
            comentario += f" - Salada: {salada}"

        # Verifica se algum comentário foi preenchido
        if not comentario:
            flash("Por favor, forneça ao menos um comentário sobre o cardápio.", "error")
            return redirect("/feedback")

        try:
            idCardapio = session.get('idCardapio')  # Melhor usar session.get para evitar KeyError
            if not idCardapio:
                flash("ID do cardápio não encontrado na sessão.", "error")
                return redirect("/feedback")

            # Conexão com o banco
            conexao, cursor = iniciar_db()
            comandoSQL = 'INSERT INTO feedback (aprovacao, comentario, idCardapio) VALUES (0, %s, %s)'
            cursor.execute(comandoSQL, (comentario, idCardapio))
            conexao.commit()

            flash("Comentário salvo com sucesso!", "success")
            return redirect("/concluido.html")

        except mysql.connector.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            flash("Erro ao acessar o banco de dados. Tente novamente.", "error")
            return redirect("/feedback")
        except Exception as e:
            print(f"Erro: {e}")
            flash(f"Ocorreu um erro inesperado: {e}", "error")
            return redirect("/feedback")
        finally:
            encerrar_db(cursor, conexao)
            
            
@app.route("/encerrar_votacao/<int:idCardapio>", methods=['POST'])
def encerrar_votacao(idCardapio):
    if not session:
        return redirect("/")

    try:
        # Inicia conexão com o banco
        conexao, cursor = iniciar_db()

        # Verifica se existe feedback associado ao cardápio
        comandoSQL = "UPDATE cardapio SET status = 0 WHERE idCardapio = %s"
        cursor.execute(comandoSQL, (idCardapio,))
        conexao.commit()
        
        # Redireciona para a página de feedback
        return redirect("/adm")
    
    except Exception as e:
        print(f"Erro ao encerrar votação: {e}")
        flash("Erro ao tentar encerrar a votação. Por favor, tente novamente.", "erro")
        return redirect("/vercardapios")
    
    finally:
        # Fecha a conexão com o banco
        encerrar_db(cursor, conexao)




#----------------- ROTA PARA VER RESULTADOS -----------------
@app.route("/resultados/<int:id_cardapio>")
def resultados(id_cardapio):
    if not session:
        return redirect("/")
    
    conexao, cursor = iniciar_db()

    try:
        # Pega os feedbacks agrupados por cardápio para exibir os resultados
        cursor.execute('SELECT COUNT(*) FROM feedback WHERE idCardapio = %s',(id_cardapio,))
        total_avaliacoes = cursor.fetchone()

        cursor.execute('SELECT COUNT(*) FROM feedback WHERE aprovacao = 1 AND idcardapio = %s',(id_cardapio,))
        numero_aprovados = cursor.fetchone()

        cursor.execute('SELECT COUNT(*) FROM feedback WHERE aprovacao = 0 AND idcardapio = %s',(id_cardapio,))
        numero_reprovados = cursor.fetchone()

        cursor.execute('SELECT comentario FROM feedback WHERE aprovacao=0 AND idcardapio = %s',(id_cardapio,))
        comentarios = cursor.fetchall()

        comandoSQL= """ 
            SELECT b.nome, sb.nome, p.nome, s.nome, c.nome, cardapio.idCardapio,    cardapio.data
            FROM cardapio
            LEFT JOIN bebida b ON b.idBebida = cardapio.idBebida
            JOIN sobremesa sb ON sb.idSobremesa = cardapio.idSobremesa
            JOIN prato_principal p ON p.idPrato_principal = cardapio.idPrato_principal
            LEFT JOIN salada s ON s.idSalada = cardapio.idSalada
            JOIN categoria c ON c.idCategoria = cardapio.idCategoria
            WHERE cardapio.idCardapio = %s
            """
        cursor.execute(comandoSQL, (id_cardapio,))  
        cardapio=cursor.fetchone()

        data_cardapio = cardapio[6].strftime('%d/%m/%Y')
        return render_template("resultados.html", total_avaliacoes=total_avaliacoes, numero_aprovados=numero_aprovados, numero_reprovados=numero_reprovados,comentarios=comentarios, cardapio=cardapio, data_cardapio=data_cardapio)
    
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/adm")
    
    finally:
        encerrar_db(cursor, conexao)
        
# ROTA PARA IMPRIMIR PDF 
        
@app.route("/gerar_pdf/<int:id_cardapio>")
def gerar_pdf(id_cardapio):
    if not session:
        return redirect("/")
    
    conexao, cursor = iniciar_db()

    try:
        # Pega os mesmos dados que são usados na página de resultados
        cursor.execute('SELECT COUNT(*) FROM feedback WHERE idCardapio = %s', (id_cardapio,))
        total_avaliacoes = cursor.fetchone()

        cursor.execute('SELECT COUNT(*) FROM feedback WHERE aprovacao = 1 AND idCardapio = %s', (id_cardapio,))
        numero_aprovados = cursor.fetchone()

        cursor.execute('SELECT COUNT(*) FROM feedback WHERE aprovacao = 0 AND idCardapio = %s', (id_cardapio,))
        numero_reprovados = cursor.fetchone()

        cursor.execute('SELECT comentario FROM feedback WHERE aprovacao=0 AND idCardapio = %s', (id_cardapio,))
        comentarios = cursor.fetchall()

        comandoSQL = """ 
            SELECT b.nome, sb.nome, p.nome, s.nome, c.nome, cardapio.idCardapio
            FROM cardapio
            LEFT JOIN bebida b ON b.idBebida = cardapio.idBebida
            JOIN sobremesa sb ON sb.idSobremesa = cardapio.idSobremesa
            JOIN prato_principal p ON p.idPrato_principal = cardapio.idPrato_principal
            LEFT JOIN salada s ON s.idSalada = cardapio.idSalada
            JOIN categoria c ON c.idCategoria = cardapio.idCategoria
            WHERE cardapio.idCardapio = %s
        """
        cursor.execute(comandoSQL, (id_cardapio,))
        cardapio = cursor.fetchone()

        # Renderiza o template para gerar o PDF, com todos os dados necessários
        return render_template(
            "imprimirPDF.html",
            total_avaliacoes=total_avaliacoes,
            numero_aprovados=numero_aprovados,
            numero_reprovados=numero_reprovados,
            comentarios=comentarios,
            cardapio=cardapio
        )
    
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return redirect("/adm")
    
    finally:
        encerrar_db(cursor, conexao)

@app.route('/concluido')
def pagina():
    return render_template('concluido.html')
        
# FINAL DO CÓDIGO - EXECUTANDO O SERVIDOR
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

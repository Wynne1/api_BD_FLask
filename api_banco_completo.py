from flask import Flask, jsonify, request, make_response
from estrutura_banco_de_dadoos import Autor, Postagem, app, db # puxando tudo que será usado 
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Definir a roda padrão: http://localhost:5000


# Definindo a função de token obrigatorio:
def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs): # ou seja indenpedente da quantidade de parâmetros que a API solicite, vai funcionar
        token = None # não possui o token ainda
        # VERIFICAR SE O TOKEN FOI ENVIADO COM AQUELA REQUISIÇÃO:
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem:':'Token não foi incluído'}, 401)
        # Se tiver token, validar acesso consultando o Banco de Dados:
        try:
            resultado = jwt.decode(token,app.config['SECRET_KEY'], algorithms=["HS256"])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first() # verificar se essas informações estão realmente cadastradas no Banco de Dados
        except:
            return jsonify({'Mensagem': 'Token inválido'}, 401)
        return f(autor, *args,**kwargs)
    return decorated
      




# Rota para autenticação:
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'}) # aparece uma tela de login para o usuário para ele preencher as informações
    #Verificar se o usuário está correto:
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    #Verificar se a senha está correta:
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow(
        ) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token':token})
    return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})





@app.route('/postagem') # significa que está na rota padrão
@token_obrigatorio

def obter_postagens(autor):
    postagens= Postagem.query.all() # puxa todos os dados de Autor
    lista_de_postagem = []
    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        lista_de_postagem.append(postagem_atual)
    return jsonify({'postagens': lista_de_postagem})


# GET com ID: http://localhost:5000/postagem/1
@app.route('/postagem/<int:id_postagem>', methods=['GET'])
@token_obrigatorio

def obter_postagem_por_id(autor,id_postagem):
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first() # apenas o primeiro resultado
    if not postagem:
        return jsonify({'Mensagem': 'Postagem não encontrada'})
    postagem_atual = {}
    try:
        postagem_atual['titulo'] = postagem.titulo
    except:
        pass
    postagem_atual['id_autor'] = postagem.id_autor

    return jsonify({'postagens': postagem_atual})


# POST : http://localhost:5000/postagem
@app.route('/postagem', methods=['POST']) 
@token_obrigatorio

def nova_postagem(autor):
    nova_postagem = request.get_json()
    postagem = Postagem(titulo=nova_postagem['titulo'], id_autor=nova_postagem['id_autor'])
    
    db.session.add(postagem)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem criada com sucesso!'})

# PUT : http://localhost:5000/postagem/1   (usa a mesma estrutura do get_id)
@app.route('/postagem/<int:id_postagem>', methods=['PUT'])
@token_obrigatorio

def alterar_postagem(autor,id_postagem):
    postagem_alterar = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    if not postagem:
        return jsonify({'Mensagem': 'Postagem não encontrada'})
    
    try:     
        postagem.titulo = postagem_alterar['titulo']
    except:
        pass

    try:
        postagem.id_autor = postagem_alterar['id_autor']
    except:
        pass

    db.session.commit()
    return jsonify({'Mensagem': 'Postagem alterada com sucesso!'})
    
# DELETE : http://localhost:5000/postagem/1   (usa a mesma estrutura do get_id)
@app.route('/postagem/<int:id_postagem>', methods=['DELETE'])
@token_obrigatorio

def excluir_postagem(autor,id_postagem):  
    postagem_excluir = Postagem.query.filter_by(id_postagem=id_postagem).first()
    if not postagem_excluir:
        return jsonify({"Mensagem": "Não foi encontrada nenhuma postagem com esse id"})
    
    db.session.delete(postagem_excluir)
    db.session.commit()

    return jsonify({'Mensagem': 'Postagem excluída com sucesso!'})

#------------------------------------------------------ API COM BANCO DE DADOS---------------------------------------------------
# GET:
@app.route('/autores')
@token_obrigatorio

def obter_autores(autor):
    autores = Autor.query.all() # puxa todos os dados de Autor
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_de_autores.append(autor_atual)
    return jsonify({'autores':lista_de_autores})

# GET_ID:
@app.route('/autores/<int:id_autor>', methods =['GET'])
@token_obrigatorio

def obter_autor_por_id(autor,id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first() # apenas o primeiro resultado
    if not autor:
        return jsonify('Autor não encontrado')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email

    return jsonify({'autor':autor_atual})

# POST:
@app.route('/autores', methods = ['POST'])
@token_obrigatorio

def novo_autor(autor):
    novo_autor = request.get_json()
    autor = Autor(nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email'])
    
    db.session.add(autor)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário criado com sucesso!'}, 200)

# PUT:
@app.route('/autores/<int:id_autor>', methods = ['PUT'])
@token_obrigatorio

def alterar_autor(autor,id_autor):
    alterar_usuario = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem': 'Usuário não encontrado'})
    
    try:     
        autor.nome = alterar_usuario['nome']
    except:
        pass

    try:
        autor.email = alterar_usuario['email']
    except:
        pass

    try:
        autor.senha = alterar_usuario['senha']
    except: 
        pass

    db.session.commit()
    return jsonify({'Mensagem': 'Usuário alterado com sucesso'})


# DELETE:
@app.route('/autores/<int:id_autor>', methods = ['DELETE'])
@token_obrigatorio

def excluir_autor(autor,id_autor):
    autor_existente = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor_existente:
        return jsonify({'Mensagem': 'Esse autor não foi encontrado'})
    
    db.session.delete(autor_existente)
    db.session.commit()

    return jsonify({'Mensagem': 'Autor excluído com sucesso!'})








# para rodar a aplicação:
if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)
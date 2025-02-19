from flask import Flask #API
from flask_sqlalchemy import SQLAlchemy #banco de dados


# O SQLALchemy transforma uma classe python em uma tabela no banco de dados


# Criar uma API flask
app = Flask(__name__)

# Criar instância SQLALchemy:
app.config['SECRET_KEY'] = '#!OUiYH6z' # acesso único à sua aplicação, colocar uma senha difícil
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///'blog.db')"

# instanciar o sqlalchemy:
db = SQLAlchemy(app)
db:SQLAlchemy # fazer essa tipagem para evitar erros

# Definir a estrutura da tabela Postagem: id_postagem, titulo, autor

class Postagem(db.Model): 
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor')) 
    


# Definir a estrutura da tabela Autor: id_autor, nome, email, senha, admin, postagens
class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean) 
    postagens = db.relationship('Postagem') 



def inicializar_banco(): # função para que o banco de dados não seja sempre dropado e criado toda vez que rodar o código
    with app.app_context():
        # Executar o comando para executar o banco de dados:
        db.drop_all() # para apagar qualquer estrutura prévia existente
        db.create_all()

        # Criar usuários administradores:
        autor = Autor(nome='Douglas', email='douglas@email.com', senha='123456', admin = True)
        db.session.add(autor)
        db.session.commit()

if __name__ =='__main__': 
    inicializar_banco()
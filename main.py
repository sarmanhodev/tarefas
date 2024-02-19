from flask import *
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from sqlalchemy import desc, asc, func
from sqlalchemy.orm import joinedload
from tables import *
from datetime import datetime, date, timedelta


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True

db = SQLAlchemy()
app = Flask(__name__, template_folder='./templates')

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}  

#STRING 
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://post_database_a0mv_user:Bm2bUZqcMfiQm5eV0Nv1Enxjg5KZbj0D@dpg-cn9p9nicn0vc738th780-a.oregon-postgres.render.com/post_database_a0mv"

app.config["SECRET_KEY"] = 'secret'
db.init_app(app)

#HOME
@app.route('/home', methods=['GET', 'POST'])
def home():
    data_atual = date.today()
    data_formatada = data_atual.strftime("%d/%m/%Y")
    #print(data_formatada)

    posts_today = db.session.query(Post).filter(Post.data_limite==data_formatada).filter(Post.post_status_id != 3).all()

    posts = db.session.query(Post).order_by(desc(Post.id)).filter(Post.data_limite != data_formatada).filter(Post.data_limite > data_formatada).filter(Post.post_status_id != 3).all()

    posts_concluidos = db.session.query(Post).order_by(desc(Post.id)).filter(Post.post_status_id == 3).all()

    posts_expirados = db.session.query(Post).order_by(desc(Post.id)).filter(Post.data_limite < data_formatada).all()

    status = db.session.query(Post_Status).order_by(asc(Post_Status.id)).all()
    
    return render_template('home.html', posts = posts,status=status,posts_today=posts_today,posts_concluidos=posts_concluidos, data_atual = data_formatada, posts_expirados=posts_expirados)


#INSERT
@app.route('/cadastrar_novo_post', methods=['GET', 'POST'])
def cadastrar_novo_post():
    dados_dict = request.get_json()

    if request.method == 'POST':
        novo_post = Post(data_post = dados_dict[0]['data_post'], data_limite = dados_dict[0]['data_limite'], data_conclusao = None, 
                         observacoes = dados_dict[0]['observacoes'],
                         post_status_id = 1, assunto = dados_dict[0]['assunto'])
        db.session.add(novo_post)
        db.session.commit()

        flash('Novo cadastro realizado com sucesso')

        return redirect(url_for('home'))


#EDITAR
@app.route('/editar_registro/<int:post_id>', methods =['GET', 'POST'])
def editar_registro(post_id):
    post = db.session.query(Post).filter(Post.id==post_id).first()
    dados_post = request.get_json()

    if request.method == 'POST':
        post.data_post = dados_post[0]['data_post']
        post.data_limite = dados_post[0]['data_limite']
        post.observacoes = dados_post[0]['observacoes']
        post.post_status_id = dados_post[0]['status']
        post.assunto = dados_post[0]['assunto']

        db.session.commit()

        flash(f'Registro atualizado com sucesso!')

        return redirect(url_for('home'))



#CONCLUIR TAREFA
@app.route("/concluir_tarefa/<int:post_id>", methods = ['GET', 'POST'])
def concluir_tarefa(post_id):
    post = db.session.query(Post).filter(Post.id==post_id).first()
    data_atual = date.today()
    data_formatada = data_atual.strftime("%d/%m/%Y")
    dados_post = request.get_json()

    if request.method == 'POST':
        post.data_conclusao = data_formatada
        post.post_status_id = dados_post[0]['status']
        db.session.commit()

        return redirect(url_for('home'))
    

#DELETAR
@app.route('/deletar_registro/<int:post_id>', methods = ['GET', 'POST'])
def deletar_registro(post_id):
    post = db.session.query(Post).filter(Post.id==post_id).first()
    db.session.delete(post)
    db.session.commit()

    flash('Registro excluído com sucesso')

    return redirect(url_for('home'))




if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')

print("Hello world")
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le3GjQbAAAAANa1sx3fbxugOBQlRDGjgP3nsKvu'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le3GjQbAAAAAJXjBb4kQb3bSPk3QRk8fqlHdHKz'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

class ImageForm(FlaskForm):
    upload = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    recaptcha = RecaptchaField()
    user = TextField()
    submit = SubmitField('Send')
 
 
def rotate_image(file_name, choice):
    im = Image.open(file_name)
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot()
    data = np.random.randint(0, 255, (100, 100))
    ax.imshow(im, cmap='plasma')
    b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
    fig.colorbar(b, ax=ax)
    gr_path = "./static/graph.png"
    sns.displot(data)
    plt.savefig(gr_path)
    plt.close()
    im = Image.open(file_name)
    x, y = im.size
    im = im.rotate(int(choice))
    im.save(file_name)

@app.route("/net", methods=['GET', 'POST'])
def image():
    form = ImageForm()
    filename = None
    filename_graph=None
    if form.validate_on_submit():
        photo = form.upload.data.filename.split('.')[-1]
        filename = os.path.join('./static', f'photo.{photo}')
        filename_graph = os.path.join('./static', f'graph.png')
        form.upload.data.save(filename)
        rotate_image(filename, form.user.data)
    return render_template('net.html', form=form, image_name=filename,filename_graph=filename_graph)

if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)

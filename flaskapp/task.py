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

class NetForm(FlaskForm):
 size = StringField('Size', validators = [DataRequired()])
 upload = FileField('Load image', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 recaptcha = RecaptchaField()
 submit = SubmitField('Send')
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

def draw(filename,size):
 print(filename)
 img= Image.open(filename)
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/graph.png"
 sns.displot(data)
 #plt.show()
 plt.savefig(gr_path)
 plt.close()
 size=int(size)
 height = 224
 width = 224
 img= np.array(img.resize((height,width)))/255.0
 print(size)
 img[:size,:,1] = (1.0,0.0,0.0)
 img[:,0:size,1] = (1.0,0.0,0.0)
 img[:,224-size:,1] = (1.0,0.0,0.0)
 img[224-size:,:,1] = (1.0,0.0,0.0)
 img = Image.fromarray((img * 255).astype(np.uint8))
 print(img)
 new_path = "./static/new.png"
 print(img)
 img.save(new_path)
 return new_path, gr_path

@app.route("/net",methods=['GET', 'POST'])
def net():
 form = NetForm()
 filename=None
 newfilename=None
 grname=None
 if form.validate_on_submit():
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  sz=form.size.data
  form.upload.data.save(filename)
  newfilename, grname = draw(filename,sz)
 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname)

if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)

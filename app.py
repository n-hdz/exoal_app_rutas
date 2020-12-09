import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pathFinder import ImageCroper, PixelReader

UPLOAD_FOLDER = 'C:\\Users\\neftali.hernandez\\Documents\\exoal_app_rutas\\static\\maps'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/mapa", methods=["POST"])
def mapa(map=None, vendedorUno=None, vendedorDos=None, colorUno=None, colorDos=None):
    if request.method == 'POST':
        if 'colonia' not in request.files:
            #flash('No se encontro archivo')
            return redirect(request.url)
        file = request.files['colonia']
        if file.filename == '':
            #flash('No se encontro archivo')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Guardar mapa en disco
            filename = secure_filename(file.filename)
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_to_file)
            # Recortar imagen
            croper = ImageCroper(path_to_file)
            croped_image = croper.crop()
            path_to_crop = os.path.join(app.config['UPLOAD_FOLDER'], 'crop_' + filename )
            croped_image.save(path_to_crop)
            # Analizar imagen
            reader = PixelReader(path_to_crop, 
                                 request.form['vendedorUnoColor'],
                                 request.form['vendedorDosColor'])
            mapped = reader.read()
            path_to_map = os.path.join(app.config['UPLOAD_FOLDER'], 'rebuilt_' + filename)
            mapped.save(path_to_map)
            map = 'rebuilt_' + filename
            # Presentar recorte para confirmar análisis
            return render_template("mapa.html", 
                                   map=map,
                                   vendedorUno=request.form['vendedorUno'],
                                   vendedorDos=request.form['vendedorDos'],
                                   colorUno=request.form['vendedorUnoColor'],
                                   colorDos=request.form['vendedorDosColor'])
# Import modul dan lib yang diperlukan
from flask import Flask, render_template, request, url_for, redirect, flash
from sklearn.cluster import MiniBatchKMeans
from matplotlib.colors import rgb2hex
from collections import Counter
from PIL import Image
import numpy as np
import os

# Setup flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'klasifikasi-warna'
app.config['UPLOAD_PATH'] = "static"
app.config['SESSION_TYPE'] = 'filesystem'


# Set laman berada
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        img = request.files["image_file"]
        if img.filename != "":
            img.save( os.path.join(app.config['UPLOAD_PATH'], img.filename) )
            
            # Buka citra yang akan diklasififikasi
            img_object = Image.open(fp=f"static/{img.filename}", mode="r")

            # Konversi citra ke 2d array
            img_array = np.array(img_object)

            # Gunakan MiniBatchKMeans algoritma dengan mengatur cluster n sebanyak 7
            k_warna = MiniBatchKMeans(n_clusters=7)
            k_warna.fit(img_array.reshape(-1, 3))

            # Hitung berapa banyak pixel per cluster
            n_pixels = len(k_warna.labels_)
            counter = Counter(k_warna.labels_)

            # 2D array yang berisi nilai pixel RGB sejumlah n cluster = 7
            rgb_int = k_warna.cluster_centers_

            # Konversi ke float 0-1
            rgb_float = np.array(rgb_int / 255, dtype=float)

            # Konversi nilai RGB ke nilai HEXA dan simpan ke dalam list
            hex_values = [rgb2hex(rgb_float[i, :]) for i in range(rgb_float.shape[0])]

            prop_warna = {}

            # Kalkulasi presentase tiap pixel warna
            for i in counter:
                prop_warna[i] = np.round(counter[i] / n_pixels, 4)

            # Konversi dictionary ke dalam list
            prop_warna = dict(sorted(prop_warna.items()))
            props_list = [value for (key, value) in prop_warna.items()]

            def to_dictionary(key, value):
                return dict(zip(key, value))

            # Merge 2 list ke dalam sebuah dictionary
            dict_warna = to_dictionary(props_list, hex_values)

            # Sort/urutkan dict secara descending
            sorted_dict = dict(sorted(dict_warna.items(), reverse=True))

            return render_template("index.html", image=img.filename, colors=sorted_dict)
        else:
            # Tampilkan error ketika belum mengunggah citra
            flash("Kamu belum mengunggah citra!")
            return redirect(url_for("home"))


# Jalankan flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)

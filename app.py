from flask import Flask
from flask import render_template, send_file, request
from pytube import YouTube
import os
import shutil
import wget
import zipfile

#Flask
app = Flask(__name__)

#Главная
@app.route("/", methods = ["post", "get"])
def index():
	#Если метод POST
	if request.method == "POST":
		#Получим ссылку
		link = request.form.get("link")
		#Создадим YouTube
		yt = YouTube(link)
		#Получим название
		title = yt.title
		#Получим путь
		path = "downloads/" + title
		#Получим описание
		description = yt.description
		#Удалим папку если она есть
		if os.path.exists(path):
			shutil.rmtree("downloads")
		#Создадим папку
		os.makedirs(path)
		#Сохраним описание
		with open(f"{path}/description.txt", "w", encoding = "utf-8") as file:
			file.write(description)
		#Превью
		thumbnail = yt.thumbnail_url.replace("sddefault", "maxresdefault")
		wget.download(thumbnail, f"{path}/preview.jpg")
		#Видео
		#yt = yt.streams.filter(progressive = True, file_extension = "mp4").order_by("resolution").desc().first()
		#yt.download(path, "video.mp4")
		#Создадим архив ZIP
		zip = zipfile.ZipFile(f"{path}/{title}.zip", "w")
		#Добавим файлы в архив ZIP
		zip.write(f"{path}/description.txt", arcname = f"{title}/description.txt")
		zip.write(f"{path}/preview.jpg", arcname = f"{title}/preview.jpg")
		#zip.write(f"{path}/video.mp4")
		#Закрываем архив ZIP
		zip.close()
		#Отдаем архив на скачивание
		return send_file(f"{path}/{title}.zip", mimetype = "application/zip")
	#Выводим шаблон
	return render_template("index.html")

if __name__ == "__main__":
	#Запустим Flask
	app.run()
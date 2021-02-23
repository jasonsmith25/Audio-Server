from flask import request, Response
import audio_metadata
from werkzeug.utils import secure_filename
import time
import os
import json
from bson import json_util
from models import *

def fileSaver(audio, audioFileType, audioFileId):
    file_name = audio.filename
    file_duration = 0
    host, paticipant, title, author, narrator = '', '', '', '', ''

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name))
    audio.save(file_path)
    metadata = audio_metadata.load(file_path)
    print(metadata)
    if 'streaminfo' in metadata:
        streaminfo = metadata['streaminfo']
        if 'duration' in streaminfo:
            file_duration = streaminfo['duration']

    if "tags" in metadata:
        tags = metadata['tags']
        if "title" in tags:
            title = str(tags["title"])
        if "albumartist" in tags:
            author = str(tags["albumartist"])
        if "artist" in tags:
            narrator = str(tags["artist"])

    ''' Here implement code for get metaData of Podcast
        but currently this type of files is not available (you can provide.)
        so i have used defalut(empty) values. thanks'''

    if audioFileType == "Song":
        if audioFileId:
            update_song = Song.query.filter_by(id=audioFileId).first()
            if file_name:
                update_song.name = file_name
            if file_duration > 0:
                update_song.duration = file_duration
            db.session.commit()
        else:
            song = Song(name=file_name, duration=file_duration)
            db.session.add(song)
            db.session.commit()
    elif audioFileType == "Podcast":
        if audioFileId:
            update_podcast = Podcast.query.filter_by(id=audioFileId).first()
            if file_name:
                update_podcast.name = file_name
            if file_duration > 0:
                update_podcast.duration = file_duration
            if host != '':
                update_podcast.host = host
            if file_name != '':
                update_podcast.paticipant = paticipant
            db.session.commit()
        else:
            podcast = Podcast(name=file_name, duration=file_duration, host=host, paticipant=paticipant)
            db.session.add(podcast)
            db.session.commit()
    elif audioFileType == "Audiobook":
        if audioFileId:
            update_audiobook = Audiobook.query.filter_by(id=audioFileId).first()
            if file_name:
                update_audiobook.title = title
            if file_duration > 0:
                update_audiobook.duration = file_duration
            if host != '':
                update_audiobook.author = author
            if file_name != '':
                update_audiobook.narrator = narrator
            db.session.commit()
        else:
            audiobook = Audiobook(title=title, duration=file_duration, author=author, narrator=narrator)
            db.session.add(audiobook)
            db.session.commit()


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return "Page Not Found!", 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return "Internal Server Error!", 500

@app.errorhandler(400)
def page_not_found(e):
    # note that we set the 400 status explicitly
    return "Bad Request!", 400

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if request.method == 'POST':
        try:
            audio = request.files.get('audio_file')
            audioFileType = request.form.get('audioFileType')
            fileSaver(audio, audioFileType, None)
            response = app.response_class(
                response=json.dumps({"message": "Data Created"}),
                status=201,
                mimetype='application/json'
            )
            return response
        except Exception as e:
            print(e)
            response = app.response_class(
                response=json.dumps({"message": "Internal Server Error"}),
                status=500,
                mimetype='application/json'
            )
        return response
    else:
        response = app.response_class(
            response=json.dumps({"message": "Method Not Allowed"}),
            status=405,
            mimetype='application/json'
        )
        return response


@app.route('/<string:audioFileType>/<int:audioFileId>', methods=['PUT'])
def update_audio(audioFileType, audioFileId):
    if request.method == 'PUT':
        try:
            audio = request.files.get('audio_file')
            fileSaver(audio, audioFileType, audioFileId)
            response = app.response_class(
                response=json.dumps({"message": "Data Updated"}),
                status=204,
                mimetype='application/json'
            )
            return response
        except Exception as e:
            print(e)
            response = app.response_class(
                response=json.dumps({"message": "Internal Server Error"}),
                status=500,
                mimetype='application/json'
            )
        return response
    else:
        response = app.response_class(
            response=json.dumps({"message": "Method Not Allowed"}),
            status=405,
            mimetype='application/json'
        )
        return response


@app.route('/<string:audioFileType>/<int:audioFileId>', methods=['GET'])
def get_one_audio(audioFileType, audioFileId):
    if request.method == 'GET':
        try:
            data = []
            if audioFileType == 'Song':
                if audioFileId:
                    song = Song.query.filter_by(id=audioFileId).first()
                    if song:
                        data = {
                            "id": song.id,
                            "name": song.name,
                            "duration": song.duration,
                            "uploaded_time": song.uploaded_time
                        }
            elif audioFileType == 'Podcast':
                if audioFileId:
                    podcast = Podcast.query.filter_by(id=audioFileId).first()
                    if podcast:
                        data = {
                            "id": podcast.id,
                            "name": podcast.name,
                            "duration": podcast.duration,
                            "uploaded_time": podcast.uploaded_time,
                            "host": podcast.host,
                            "paticipant": podcast.paticipant
                        }
            elif audioFileType == 'Audiobook':
                if audioFileId:
                    audiobook = Audiobook.query.filter_by(id=audioFileId).first()
                    if audiobook:
                        data = {
                            "id": audiobook.id,
                            "title": audiobook.title,
                            "duration": audiobook.duration,
                            "uploaded_time": audiobook.uploaded_time,
                            "author": audiobook.author,
                            "narrator": audiobook.narrator
                        }

            response = app.response_class(
                response=json.dumps(data, default=json_util.default),
                status=200,
                mimetype='application/json'
            )
            return response
        except Exception as e:
            print(e)
            response = app.response_class(
                response=json.dumps({"message": "Internal Server Error"}),
                status=500,
                mimetype='application/json'
            )
        return response
    else:
        response = app.response_class(
            response=json.dumps({"message": "Method Not Allowed"}),
            status=405,
            mimetype='application/json'
        )
        return response


@app.route('/<string:audioFileType>', methods=['GET'])
def get_all_audio(audioFileType):
    if request.method == 'GET':
        try:
            data = []
            if audioFileType == 'Song':
                songs = Song.query.all()
                for song in songs:
                    data.append({
                        "id": song.id,
                        "name": song.name,
                        "duration": song.duration,
                        "uploaded_time": song.uploaded_time
                    })
            elif audioFileType == 'Podcast':
                podcasts = Podcast.query.all()
                for podcast in podcasts:
                    data.append({
                        "id": podcast.id,
                        "name": podcast.name,
                        "duration": podcast.duration,
                        "uploaded_time": podcast.uploaded_time,
                        "host": podcast.host,
                        "paticipant": podcast.paticipant
                    })
            elif audioFileType == 'Audiobook':
                audiobooks = Audiobook.query.all()
                for audiobook in audiobooks:
                    data.append({
                        "id": audiobook.id,
                        "title": audiobook.title,
                        "duration": audiobook.duration,
                        "uploaded_time": audiobook.uploaded_time,
                        "author": audiobook.author,
                        "narrator": audiobook.narrator
                    })

            response = app.response_class(
                response=json.dumps(data, default=json_util.default),
                status=200,
                mimetype='application/json'
            )
            return response
        except Exception as e:
            print(e)
            response = app.response_class(
                response=json.dumps({"message": "Internal Server Error"}),
                status=500,
                mimetype='application/json'
            )
        return response
    else:
        response = app.response_class(
            response=json.dumps({"message": "Method Not Allowed"}),
            status=405,
            mimetype='application/json'
        )
        return response


@app.route('/<string:audioFileType>/<int:audioFileId>', methods=['DELETE'])
def remove_audio(audioFileType, audioFileId):
    if request.method == 'DELETE':
        try:
            data = {}
            if audioFileType == 'Song':
                if audioFileId:
                    Song.query.filter_by(id=audioFileId).delete()
                    db.session.commit()
            elif audioFileType == 'Podcast':
                if audioFileId:
                    Padcast.query.filter_by(id=audioFileId).delete()
                    db.session.commit()
            elif audioFileType == 'Audiobook':
                if audioFileId:
                    Audiobook.query.filter_by(id=audioFileId).delete()
                    db.session.commit()

            response = app.response_class(
                response=json.dumps({"message": "Audio Deleted"}),
                status=202,
                mimetype='application/json'
            )
            return response
        except Exception as e:
            print(e)
            response = app.response_class(
                response=json.dumps({"message": "Internal Server Error"}),
                status=500,
                mimetype='application/json'
            )
        return response
    else:
        response = app.response_class(
            response=json.dumps({"message": "Method Not Allowed"}),
            status=405,
            mimetype='application/json'
        )
        return response
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

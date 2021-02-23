# Create API
Method: POST
URL : http://127.0.0.1:5000/upload-audio
from-data : {
	"audio_file" : <audio_file>.mp3,
	"audioFileType" : "Song"		#( it can be "Song, Podcast, Audiobook")
	}

# Update API
Method: PUT
URL : http://127.0.0.1:5000/<audio_file_type>/<audio_file_id>
from-data : {
	"audio_file" : <audio_file>.mp3
	}


# Get API
Method: GET
URL : http://127.0.0.1:5000/<audio_file_type>/<audio_file_id> OR http://127.0.0.1:5000/<audio_file_type>


# Delete API
Method: DELETE
URL : http://127.0.0.1:5000/<audio_file_type>/<audio_file_id>

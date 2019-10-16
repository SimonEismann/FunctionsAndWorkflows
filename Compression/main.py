from pydub import AudioSegment
from io import BytesIO
import os

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # This code will process each file uploaded
    file = request.files["to_compress"]
    # find out length of file
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    #reset file
    file.seek(0)
    print("Inputfilesize: "+str(file_length))
    outputfile=BytesIO()
    speech = AudioSegment.from_wav(file)
    speech = speech.set_frame_rate(5000)
    speech = speech.set_sample_width(1)
    speech.export(outputfile, format="wav")
    
    # print file lengths
    #print("Inputfilesize: "+str(file_length))
    print("Outputfilesize: "+str(len(outputfile.getvalue())))
    
    return outputfile.getvalue()
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
    input = BytesIO(request.data)
    inputSize = len(input.getvalue())
    speech = AudioSegment.from_mp3(input)
    output = BytesIO()
    speech.export(output, format="wav")

    print("Inputfilesize: " + str(inputSize))
    print("Outputfilesize: " + str(len(output.getvalue())))

    return output.getvalue()
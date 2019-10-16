from pydub import AudioSegment
from io import BytesIO
import numpy as np
import os
import json

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    indexes = json.load(request.files["indexes"])
    file = request.files["to_censor"]
    # find out length of file
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    #reset file
    file.seek(0)
    print("Inputfilesize: "+str(file_length))
    print("Length of Input-Indexes: "+str(len(indexes)))
    outputfile=BytesIO()
    speech = AudioSegment.from_wav(file)
    
    samples = np.array(speech.get_array_of_samples())
    # efficient implementation
    #for start, end in indexes:
    #    start_sample = int(start*len(samples))
    #    end_sample = int(end*len(samples))
    #    samples[start_sample:end_sample] = [0]
    
    # we use the inefficient implementation here
    for index, s in enumerate(samples):
        for start, end in indexes:
            start_sample = int(start*len(samples))
            end_sample = int(end*len(samples))
            if index > start_sample and index < end_sample:
                samples[index] = 0
    
    new_sound = speech._spawn(samples)
    new_sound.export(outputfile, format="wav")      
          
    # print file lengths
    print("Outputfilesize: "+str(len(outputfile.getvalue())))
    
    return outputfile.getvalue()
def readSRTFile(file_name):
    file_name += ".srt"
    file = open( file_name, encoding='utf-8')
    lines = file.readlines()
    file.close()
    return lines

def writeSRTFile(title,array,space):
    srtDocument= open(title+".srt","w+",encoding="utf-8")
    if space:
        for line in array:
            srtDocument.write(str(line)+"\n")
    else:
        for line in array:
            srtDocument.write(str(line))
    srtDocument.close()
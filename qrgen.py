import  qrcode
def qrgenerator(url:str, id:str):
    data = url
    filename = id
    img = qrcode.make(data)
    img.save(filename)
    return True
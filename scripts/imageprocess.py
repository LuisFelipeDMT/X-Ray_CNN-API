import os
import glob
from PIL import Image
import numpy as np
from urllib import request
from random import randint

def compile_model(model,optimizer,metrics):
    model.compile(loss = 'categorical_crossentropy',
                  optimizer = optimizer,
                  metrics = metrics)
    return model

def load_model():
    global model
    import os
    from tensorflow.keras.models import model_from_json
    from tensorflow.keras.optimizers import Adam
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    try:
        model = model_from_json(loaded_model_json)
        model.load_weights('model_weights.h5')
        print('Modelo carregado com sucesso')
    except:
        print('Erro, o modelo ou pesos não estão acessíveis.')
    metrics=['accuracy']
    Learning_rate=0.01
    adam = Adam(learning_rate = Learning_rate)
    compile_model(model, adam, metrics)
    
def predict_image(imageLink):
    
    try:
        globals()['model']
    except:
        load_model()
    localfile='img'+str(randint(0, 1000000000))+".png"
    request.urlretrieve(imageLink, localfile)
    categories=['COVID','Lung_Opacity','Normal','Viral Pneumonia']
    # open and adjust image format and size
    im=Image.open(localfile)
    rgb_im = im.convert('RGB')
    imResize = rgb_im.resize((256,256), Image.ANTIALIAS)
    #convert image to array and normalize
    im=np.asarray(imResize)
    im=im/255
    os.remove(localfile)
    #make prediction
    prob=model.predict(np.asarray([im]))*100
    position=np.argmax(prob)
    prob=prob.tolist()[0]
    for index,item in enumerate(prob):
        prob[index]=round(item)    
    position=np.argmax(model.predict(np.asarray([im])))
    disease=categories[position]

    return prob, categories, disease
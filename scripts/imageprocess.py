import os
from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import Adam
import glob
from PIL import Image
import numpy as np

def compile_model(model,optimizer,metrics):
    model.compile(loss = 'categorical_crossentropy',
                  optimizer = optimizer,
                  metrics = metrics)
    return model

def predict_image(image):

    categories=['COVID','Lung_Opacity','Normal','Viral Pneumonia']
    metrics=['accuracy']
    Learning_rate=0.01
    adam = Adam(learning_rate = Learning_rate)

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
    compile_model(model, adam, metrics)

    # open and adjust image format and size
    im=Image.open(image)
    rgb_im = im.convert('RGB')
    imResize = rgb_im.resize((256,256), Image.ANTIALIAS)
    #convert image to array and normalize
    im=np.asarray(imResize)
    im=im/255
    #make prediction 
    proba=np.max(model.predict_proba(np.asarray([im])))*100
    position=np.argmax(model.predict_proba(np.asarray([im])))
    disease=categories[position]

    return proba, disease
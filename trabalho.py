from tkinter import filedialog
from tkinter import *
import os
from pydub import AudioSegment
import shutil
import matplotlib.pyplot as plt
import numpy as np
import wave

def plotting(arquivo,modo):

    file = arquivo

    wav_file = wave.open(file, 'r')

    # Extrai arquivo Raw Audio para Wav
    sinal = wav_file.readframes(-1)
    if wav_file.getsampwidth() == 1:
        sinal = np.array(np.frombuffer(sinal, dtype='UInt8') - 128, dtype='Int8')
    elif wav_file.getsampwidth() == 2:
        sinal = np.frombuffer(sinal, dtype='Int16')
    else:
        raise RuntimeError("Tamanho do sample não definido")

    deinterleaved = [sinal[idx::wav_file.getnchannels()] for idx in range(wav_file.getnchannels())]

    #Pega tempo dos indices
    fs = wav_file.getframerate()
    Time = np.linspace(0, len(sinal) / wav_file.getnchannels() / fs, num=len(sinal) / wav_file.getnchannels())

    # Plot
    plt.figure(1)
    plt.title("Signal wave:"+modo)
    for channel in deinterleaved:
        plt.plot(Time, channel)
    plt.show()


#criação dos diretoriios para funcionar o progrmar
if os.path.exists("musicas")== False:
    os.makedirs("musicas")

if os.path.exists("mono") == False:
    os.makedirs("mono")

#utilização da GUI TKinter
root = Tk()

#abrir selecionador de arquivos do windows, somente arquivos mp3 e wav(pode ser mais de um)
files = list(filedialog.askopenfilenames(parent=root, title='Selecione um arquivo estéreo', filetypes=(("wav files", "*.wav"),("All files", "*.*"))))

#salvar na variavel os cominhos dos arquivos da pasta musicas
pasta = os.listdir('musicas')

listMusicas=[]
#verificação para saber se existe mais arquivos para haver a renomeação
if pasta:
    ultNumeroDivid=pasta[len(pasta)-1].split(".")
    ultNumero=int(ultNumeroDivid[0])
else:
    ultNumero = 0
i = 0

while i < len(files):
    ultNumero += 1

    arqDiv=str(files[i]).split(".")
    formatAqv=arqDiv[len(arqDiv)-1]

    if formatAqv == "wav" :
        #renomeando o arquivo para ser salvo em outra pasta pelo numero
        listMusicas.append('musicas/'+str(ultNumero)+".wav")

        #copiando para outra pasta, ja renomado
        shutil.copy(files[i], listMusicas[i])

        plotting(listMusicas[i],listMusicas[i]+" em Estéreo")

        # selecionando o arquivo, transformando pra mono, e exportando para pasta mono
        sound= AudioSegment.from_wav(listMusicas[i])
        sound = sound.set_channels(1)
        caminhoMono = "mono/" + str(ultNumero) + ".wav"
        sound.export(caminhoMono, format("wav"))

        plotting(caminhoMono,caminhoMono+" em Mono")

    i += 1


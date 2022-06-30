import discord
from discord.ext import commands
import numpy as np
import tflearn
import tensorflow as tf
import random
import pickle
import string
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Flatten, GlobalMaxPool1D
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import string


bot = commands.Bot(command_prefix=".")

responses = {'greeting': ['VO_Yae_Miko_Hello.ogg'],
 'hobbies': ['VO_Yae_Miko_Hobbies.ogg'],
 'about you': ['VO_Yae_Miko_More_About_Yae_Miko_-_01.ogg',
  'VO_Yae_Miko_More_About_Yae_Miko_-_02.ogg',
  'VO_Yae_Miko_More_About_Yae_Miko_-_03.ogg',
  'VO_Yae_Miko_More_About_Yae_Miko_-_05.ogg'],
 'about vision': ['VO_Yae_Miko_About_the_Vision.ogg'],
 'about us': ['VO_Yae_Miko_About_Us_-_Erosion.ogg'],
 'eternity': ['VO_Yae_Miko_About_Yae_Miko_-_Eternity.ogg']}


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        ctx = await bot.get_context(message)
        if(ctx.author.voice):
            if(ctx.voice_client):
                await ctx.voice_client.move_to(ctx.author.voice.channel)
            else:
                await ctx.author.voice.channel.connect()
            prediction_input = message.content.split(" ", 1)[1]
            texts = []
            prediction_input = [letter.lower() for letter in prediction_input if letter not in string.punctuation]
            prediction_input = ''.join(prediction_input)
            texts.append(prediction_input)
            prediction_input = tokenizer.texts_to_sequences(texts)
            prediction_input = np.array(prediction_input).reshape(-1)
            prediction_input = pad_sequences([prediction_input], 6)
            output = model.predict(prediction_input)
            outputindex = np.argmax(output)
            response_tag = LE[outputindex]
            voice_file = random.choice(responses[response_tag])
            source = discord.FFmpegPCMAudio(source="Yae Miko\{}".format(voice_file), executable='C:\\ffmpeg\\bin\\ffmpeg.exe')
            player = ctx.voice_client.play(source)
        else:
            await ctx.send("You are not connected to the voice channel")

@bot.event
async def on_connect():
    global model
    global tokenizer
    global LE

    try:
        model = tf.keras.models.load_model('yaemikomodel.h5')
        print("Model loaded !")
    except:
        print("Model failed to load !")

    try:
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        print("tokenizer loaded !")
    except:
        print("tokenizer failed to load")

    try:
        with open('LE.pickle', 'rb') as handle:
            LE = pickle.load(handle)
        print("Label Encoder loaded !")
    except:
        print("Label Encoder failed to load")

    print("bot connected to discord !")

TOKEN = 'ODkxNTM5NDI0OTk3OTU3NjMy.YU_0yg.a2U303IhdBvKhNXBsWf9p81xKrk'

bot.run(TOKEN)








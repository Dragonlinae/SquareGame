import numpy
import pickle
import os

def save(guild, arr, dimension):
  numpy.save("Ω" + guild + "_" + dimension, arr)

def load(guild, dimension):
  return numpy.load("Ω" + guild + "_" + dimension + ".npy", allow_pickle=True)

def savesetting(guild, settings):
  
  with open("Ω" + guild + "_settings" + ".pkl", 'wb') as file:
    pickle.dump(settings, file)

def loadsetting(guild):
  try:
    with open("Ω" + guild + "_settings" + ".pkl", 'rb') as file:
      return pickle.load(file)
  except:
    savesetting(guild, [1, 0, 0, 0, 0, 3, 0, 8, 8, 0, 0, None, None, "overworld"])
    return loadsetting(guild)
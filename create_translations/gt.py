# File to translate the abbrev, colloq, proper, and variant texts with Google Translate

import os

from googletrans import Translator

translator = Translator()
sample_text = "こちら葛飾区亀有公園前派出所が連載続いてたら"
translation = translator.translate(sample_text, src='ja', dest='en')
print(translation.text)
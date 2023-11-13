# keywords_dict[base key] = the code itself
# trans_dict[base_key] = the wanted code
# Goal is to build a new dict with the current code as key and wanted word as value
##############################
# Imports
##############################
import json
import sys
import os

##############################
# Constants
##############################

generate = False
magic_dict = dict()  # The dict that has the right keys and values
is_string = False
quotes_count = 0
word = ""
code = ""
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
#print(keywords)
with open(f"{app_path}/keywords.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)["keywords"][0]
##############################
# Main Cls
##############################
class Translate:
    def __init__(self, text):
        self.text = text
        self.idx = -1
        self.current_char = None
        self.next_char()
    def next_char(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.current_char = self.text[self.idx]
        else:
            self.current_char = None
            code = ""
    def generate_right_dict(self, lang):
        global generate
        with open(f"{app_path}/data/{lang}_KW.json", "r", encoding="utf-8") as f:
            trans = json.load(f)["keywords"][0]
        for i in keywords:
            magic_dict[keywords[i]] = trans[i]
            #print(magic_dict)
        generate = True


        #print(trans)
    def translate(self, lang):
        if not generate:
            self.generate_right_dict(lang)
        global word
        global code
        global magic_dict
        word = word.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
        #print(word)
        try:
            code += magic_dict[word]
        except:
            code += word
        #print(code)



    def read(self, lang):
        global is_string
        global quotes_count
        global word
        global code
        while True :
            if self.current_char != None:
                if self.current_char in ("'", '"'):
                    code += '"'
                    quotes_count += 1
                if quotes_count % 2 != 0:
                    is_string = True
                else:
                    is_string = False
                # print(self.current_char)
                #print(is_string)
                if not is_string:
                    word += self.current_char
                    #print(word)
                    if self.current_char in " \t()\n":
                        self.translate(lang=lang)
                        code += self.current_char
                        word = ""
                else:
                    if self.current_char != "'" and self.current_char != '"' and self.current_char:
                        code += self.current_char

                self.next_char()
            else:
                return code
                break

# test_object = Translate("""
# var a = 10
# var b = 20
# print(a+b)
# var x = int_input()
# print("var x = ")
# print(x)
# """)
# print(test_object.read("Arabic"))

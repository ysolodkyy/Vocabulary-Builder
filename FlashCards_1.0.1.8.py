# License: http://creativecommons.org/licenses/by-sa/3.0/	

import tkinter as tk
from utils import save_list, open_newlist
import random
from tkinter import messagebox
from macos_speech import Synthesizer

LARGE_FONT= ("Roman", 17)

words_list = [] # originally opened list
weights = [] # weights for words_list 

current_word = {}

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, FlashCards):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        global words_list, weights

        if cont == StartPage: 
            save_list(StartPage.word_length, words_list, weights)

        elif cont == FlashCards:
            words_list, weights = open_newlist(StartPage.word_length)
        else: 
            print("should never occur")

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame, Application):

    word_length = 2
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Select Word Length", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.spinbox = tk.Spinbox(self,from_ = 2, to = 13, width = 5, command = self.spinbox_selection )
        self.spinbox.pack()

        button2 = tk.Button(self, text="Start Learning", command=lambda: controller.show_frame(FlashCards))
        button2.pack()
    
    def spinbox_selection(self):
        StartPage.word_length = self.spinbox.get()


class FlashCards(tk.Frame, Application):

    message = f"press: \n>>'Next' for next word,\n>>'Know' for if know the word,\n>>'Flip Card' to see definition\n>>'No. Words' for total words in current list"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.front_flag = True

        # create text 
        self.text_box = tk.Text(self, height=10, width=45, font = LARGE_FONT, wrap = tk.WORD)
        self.text_box.insert(tk.END, self.message)
        self.text_box.configure(state='disabled')
        self.text_box.grid(row = 1, column = 0, padx = 3, pady = 3, columnspan = 3)

        # create buttons

        button1 = tk.Button(self, text="Home", command=self.refresh)
        button1.grid(row = 0, column = 2, padx = 3, pady = 3)

        button2 = tk.Button(self, text="No. Words in List", command=self.word_count)
        button2.grid(row = 0, column = 0, padx = 3, pady = 3)
        
        button3 = tk.Button(self, text="Know", command=self.update_to_learn_list)
        button3.grid(row = 2, column = 0, padx = 3, pady = 3)
        
        button4 = tk.Button(self, text="Flip Card", command=self.flip_card)
        button4.grid(row = 2, column = 1, padx = 3, pady = 3)

        button5 = tk.Button(self, text="Next Word", command=self.show_next_word)
        button5.grid(row = 2, column = 2, padx = 3, pady = 3)
        
        button6 = tk.Button(self, text="Speak", command=self.speak)
        button6.grid(row = 0, column = 1, padx = 3, pady = 3)

    def word_count(self):
        self.front_flag = True
        self.update_text(f"No. words in the list: {len(words_list)}")

    def flip_card(self):
        global current_word
        if len(current_word) == 0:
            pass
        else:
            if self.front_flag == True:
                self.update_text("\n\n\n\n\t\t\t"+ current_word['word'].upper())
                self.front_flag = False
            else:
                self.update_text(current_word['definition']) 
                self.front_flag = True

    def show_next_word(self):
        '''randomly select a word from the list according to the weights'''

        global current_word, weights, words_list
        try:
            current_word = random.choices(words_list, weights = weights, k = 1)[0] 

        except IndexError as error_message:
            # throw exception if the words_list is empty
            print(f"{error_message}: the list is empty!")
            current_word = {} # clear current word
            self.update_text(f"the list is empty! no more words to learn!") 

        else:
            self.update_text("\n\n\n\n\t\t\t"+ current_word['word'].upper())
            self.front_flag = False

    def update_to_learn_list(self):
        '''reduce the weight of the word marked as known'''
        global current_word, weights, words_list

        if len(current_word) == 0 or len(words_list) == 0 :
            # do nothing if no current word selected or if worlds_list is exhausted
            pass
        else:
            idx = words_list.index(current_word) # get the index of the current word
            print(f"current {current_word['word']}'s weight:{weights[idx]}")

            # update the weight of the word
            if weights[idx] > 1:
                weights[idx] -=1
                print(f"updated {current_word['word']}'s weight:{weights[idx]}")
                # show next word
                self.show_next_word() 
            else:
                tk.messagebox.showinfo(title="Attention", message=f"You've learned '{current_word['word']}' !", icon='info')
                # remove the idx entry from both weights and words_list. 
                del weights[idx]
                del words_list[idx]
                try:
                    len(weights) == len(words_list)
                except ValueError:
                    print("The lists are not the same length! ")
                self.show_next_word()

    def refresh(self):
        global current_word
        current_word = {} # clear current_word for fresh start
        self.update_text(self.message)
        self.controller.show_frame(StartPage)

    def speak(self):
        global current_word
        if len(current_word) == 0:
            pass
        else:
            speaker = Synthesizer(voice='Alex', device='Built-in')
            speaker.text = current_word['word']
            speaker.talk()

    def update_text(self, txt):

        self.text_box.configure(state='normal')
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, txt)
        self.text_box.configure(state='disabled')



if __name__ == "__main__":

    app = Application()
    app.mainloop()
    # save the list in case the app window is simply closed
    save_list(StartPage.word_length, words_list, weights)

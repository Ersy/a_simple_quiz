import csv
import random
import tkinter as tk
import copy
from tkinter import filedialog

class Main:
    def __init__(self, master):

        self.master = master
        self.master.title("Fun Quiz!")
        self.var_filename = tk.StringVar()

        self.number_of_rounds = tk.IntVar()
        self.number_of_rounds.set(5)

        self.user_defined = tk.BooleanVar()
        self.user_defined.set(0)

        self.real_answer = tk.StringVar()
        self.previous_answer = tk.StringVar()

        self.correct = tk.IntVar()
        self.total = tk.IntVar()
        self.correct.set(0)
        self.total.set(0)

        self.question_text = tk.StringVar()

        self.answer_list = [tk.StringVar(), tk.StringVar(), tk.StringVar(),
                            tk.StringVar(), tk.StringVar()]

        self.live_question = tk.StringVar()

        self.load_quiz()

### Widgets ###
        container = tk.Frame(master, padx = 5, pady = 5)

        labelview_left = tk.LabelFrame(container, text = "Quiz", padx = 5, pady = 5)
        labelview_right = tk.LabelFrame(container, text = "Options", padx = 5, pady = 5)

        quiz_question_text = tk.Label(labelview_left, textvariable = self.question_text)

        quiz_question = tk.Label(labelview_left, textvariable = self.live_question)


        self.answer_buttons = []
        for i in range(len(self.answer_list)):
            self.answer_buttons.append(tk.Button(labelview_left,
                                                 textvariable=self.answer_list[i],
                                                 command = lambda i=i: self.is_it_correct(i),
                                                 width = 10))



        reset_button = tk.Button(labelview_right, text= "Reset Score",
                                 command = lambda: self.reset_quiz(),
                                 width = 20)

        button_filepath = tk.Button(labelview_right,
                                    text = "Load quiz from file",
                                    command=lambda: self.browse_file(),
                                    width = 20)

        button_default_quiz = tk.Button(labelview_right,
                                        text = "Use default quiz",
                                        command=lambda: self.default_quiz(),
                                        width = 20)


        correct_answer_text = tk.Label(labelview_right,
                                       text = "The correct answer was ")

        correct_answer_label = tk.Label(labelview_right,
                                        textvariable = self.previous_answer)



        correct_text = tk.Label(labelview_right, text = "Correct: ")
        total_text = tk.Label(labelview_right, text = "Total: ")
        correct_label = tk.Label(labelview_right, textvariable = self.correct)
        total_label = tk.Label(labelview_right, textvariable = self.total)

### Positioning of Widgets ###
        container.pack(expand = True)

        labelview_left.grid(row = 0, column = 0, sticky=tk.NSEW)
        labelview_right.grid(row = 0, column = 4, sticky=tk.NSEW)

### Left labelview ##
        quiz_question_text.grid(row=0)
        quiz_question.grid(row=1)

        for i in range(len(self.answer_buttons)):
            self.answer_buttons[i].grid(row = i+2, columnspan = 1)

## Right Labelview ##
        reset_button.grid(row = 0, column = 0, sticky=tk.N)

        button_filepath.grid(row = 1, column = 0, sticky=tk.NSEW)
        button_default_quiz.grid(row = 2, column = 0, sticky=tk.NSEW)


        correct_text.grid(row = 5)
        correct_label.grid(row = 6)
        total_text.grid(row = 7)
        total_label.grid(row = 8)


        correct_answer_text.grid(row = 9)
        correct_answer_label.grid(row = 10)
### Methods ###

    def load_quiz(self):
        self.reset_quiz()
        quiz = Quiz_getter(self.user_defined)
        #If user_defined is true, gets the quiz from csv, if false gets the default quiz
        quiz_title, quiz_dict =  quiz.get_quiz(self.var_filename.get())
        self.live_quiz = Quiz(quiz_dict)
        self.question_text.set(quiz_title)
        self.load_question()


    def load_question(self):
        live_question, real_answer, live_all_answers = self.live_quiz.gen_new_question()
        self.live_question.set(live_question)
        self.real_answer.set(real_answer)
        for i in range(len(self.answer_list)):
            self.answer_list[i].set(live_all_answers[i])

    def browse_file(self):
        """User selects the text file to load user_defined flag is switched to true and the select quiz is loaded"""
        path = filedialog.askopenfilename(filetypes=[("allfiles","*"),("comma separated value","*.csv")])
        if not path:
            return
        self.var_filename.set(path)
        self.user_defined = True
        self.load_quiz()

    def default_quiz(self):
        """Changes the quiz back to the default"""
        self.user_defined = False
        self.filename = None
        self.load_quiz()


    def is_it_correct(self, num):
        """compares selected answer with actual answer"""
        if self.answer_list[num].get() == self.real_answer.get():
            self.correct.set( self.correct.get() + 1 )
        self.total.set(self.total.get() + 1)
        self.previous_answer.set(self.real_answer.get())
        self.load_question()


    def reset_quiz(self):
        """Resets the score"""
        self.correct.set(0)
        self.total.set(0)



### GAME STUFF ###

class Quiz_getter:
    def __init__(self, user_quiz):
        self.user_quiz = user_quiz

        #This is the default quiz
        self.countries_title = "What is the capital city of "
        self.countries_quiz = {"Afghanistan": "Kabul",
                  "Bulgaria": "Sofia", "Pakistan": "Islamabad",
                  "Chad": "N'Djamena", "Hungary": "Budapest",
                  "England":"London", "Jordan":"Amman", "Kenya":"Nairobi",
                  "Canada":"Ottawa", "Norway":"Oslo", "Taiwan":"Taipei"}


    def get_quiz(self, user_path):
        if self.user_quiz == True:
            try:
                with open(user_path, mode = 'r') as file:
                    reader = csv.reader(file)
                    title = (reader.__next__())[0]
                    user_QA = dict((row[0], row[1]) for row in reader)
                return title, user_QA
            except Exception as e:
                print (e)
                return self.countries_title, self.countries_quiz
        else:
            return self.countries_title, self.countries_quiz



class Quiz:
    def __init__(self, quiz):
        self.quiz = quiz


#from the current quiz dictionary, make a copy of the quiz
#select a random key value pair as the question and answer
#remove the question and answer from the copied quiz
#randomly select 4 more 'incorrect' answers from the quiz as a new list
#add the real answer to the list
#return the question along with the list of answers
    def gen_new_question(self):
        """
        Generates 'question' from the quiz along with the correct answer
        and 4 incorrect answers.
        """
        quiz = copy.deepcopy(self.quiz)
        question = random.choice(list(quiz))
        real_answer = quiz[question]
        del quiz[question]
        all_answers = random.sample(list(quiz.values()),4)
        all_answers.extend([real_answer])
        random.shuffle(all_answers)
        return question, real_answer, all_answers



if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
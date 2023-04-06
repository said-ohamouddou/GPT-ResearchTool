#import required libraries and modules
import sys
import os
import openai
import pyperclip
from PyQt6.QtWidgets import (
QApplication, QWidget, QVBoxLayout, QHBoxLayout,
QPushButton, QLineEdit, QTextEdit, QMessageBox
)
from qt_material import apply_stylesheet

#Set up OpenAI API key
openai.api_key = "Your openai API Key "

#Define main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Set up window properties
        self.setWindowTitle("GptResearchTool")
        self.setFixedWidth(510)
        self.setFixedHeight(550)

        # Set up input and output text boxes
        self.input_text = QTextEdit()
        self.input_text.setFixedHeight(150)
        self.input_text.setPlaceholderText('Input')
        self.output_text= QTextEdit()
        self.output_text.setFixedHeight(150)
        self.output_text.setPlaceholderText('Output')

        # Set up target language input box
        self.target_languge = QLineEdit()
        self.target_languge.setPlaceholderText('Language')

        # Set up buttons for various functionalities
        self.translation_btn = QPushButton()
        self.translation_btn.setText("Translate")
        self.translation_btn.clicked.connect(lambda: self.translate())

        self.rephrase_btn = QPushButton()
        self.rephrase_btn.setText("Rephrase")
        self.rephrase_btn.clicked.connect(lambda: self.rephrase())

        self.grammar_check_btn = QPushButton()
        self.grammar_check_btn.setText("Check grammar")
        self.grammar_check_btn.clicked.connect(lambda: self.grammar_check())
        self.summarize_btn = QPushButton()
        self.summarize_btn.setText("Summarize")
        self.summarize_btn.clicked.connect(lambda: self.summarize())

        self.suggest_title_btn = QPushButton()
        self.suggest_title_btn.setText("Suggest title")
        self.suggest_title_btn.clicked.connect(lambda: self.suggest_title())

        self.suggest_references_btn = QPushButton()
        self.suggest_references_btn.setText("References")
        self.suggest_references_btn.clicked.connect(lambda: self.suggest_references())

        self.suggest_studies_btn = QPushButton()
        self.suggest_studies_btn.setText("Studies")
        self.suggest_studies_btn.clicked.connect(lambda: self.suggest_studies())

        self.get_research_question_btn = QPushButton()
        self.get_research_question_btn.setText("Research questions")
        self.get_research_question_btn.clicked.connect(lambda: self.get_research_question())

        self.get_hypothesis_btn = QPushButton()
        self.get_hypothesis_btn.setText("Hypothesis")
        self.get_hypothesis_btn.clicked.connect(lambda: self.get_hypothesis())

        self.test_hypothesis_btn = QPushButton()
        self.test_hypothesis_btn.setText("Test hypothesis")
        self.test_hypothesis_btn.clicked.connect(lambda: self.test_hypothesis())

        self.interpret_results_btn = QPushButton()
        self.interpret_results_btn.setText("Interpret")
        self.interpret_results_btn.clicked.connect(lambda: self.interpret_results())

        self.more_information_btn = QPushButton()
        self.more_information_btn.setText("More information")
        self.more_information_btn.clicked.connect(lambda: self.more_information())

        self.just_send_btn = QPushButton()
        self.just_send_btn.setText("Just send")
        self.just_send_btn.clicked.connect(lambda: self.just_send())

        self.copy_btn = QPushButton()
        self.copy_btn.setText("Copy")
        self.copy_btn.clicked.connect(lambda: self.copy_output())

        self.clear_btn = QPushButton()
        self.clear_btn.setText("Clear")
        self.clear_btn.clicked.connect(lambda:self.clear_output())

        #Create a QPushButton and set its text and connect its clicked signal to a method
        self.set_output_as_input_btn= QPushButton()
        self.set_output_as_input_btn.setText("Set as input")
        self.set_output_as_input_btn.clicked.connect(lambda: self.set_output_as_input())

        #Create several QHBoxLayouts and add QPushButtons to them
        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.rephrase_btn)
        button_layout1.addWidget(self.grammar_check_btn)
        button_layout1.addWidget(self.get_research_question_btn)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.target_languge)
        button_layout2.addWidget(self.translation_btn)
        button_layout2.addWidget(self.summarize_btn)
        button_layout2.addWidget(self.suggest_studies_btn)

        button_layout3 = QHBoxLayout()
        button_layout3.addWidget(self.suggest_references_btn)
        button_layout3.addWidget(self.suggest_title_btn)
        button_layout3.addWidget(self.more_information_btn)

        button_layout4 = QHBoxLayout()
        button_layout4.addWidget(self.get_hypothesis_btn)
        button_layout4.addWidget(self.test_hypothesis_btn)
        button_layout4.addWidget(self.interpret_results_btn)
        button_layout4.addWidget(self.just_send_btn)

        button_layout5 = QHBoxLayout()
        button_layout5.addWidget(self.copy_btn)
        button_layout5.addWidget(self.set_output_as_input_btn)
        button_layout5.addWidget(self.clear_btn)

        #Create two QVBoxLayouts and add the QTextEdit widgets and QHBoxLayouts to them
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.input_text)
        output_layout = QVBoxLayout()
        output_layout.addWidget(self.output_text)

        #Create a main QVBoxLayout to hold all the other layouts
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout1)
        main_layout.addLayout(button_layout2)
        main_layout.addLayout(button_layout3)
        main_layout.addLayout(button_layout4)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout5)

        #Set the main layout for the window
        self.setLayout(main_layout)
        #Set the initial value of a class variable
        self.request=None

    def rephrase(self):
        self.request="Rephrase this paragraph " # Set the request
        self.send_to_chatgpt() # Send the request to ChatGPT

    # Function to summarize the input paragraph
    def summarize(self):
        self.request="summarize this paragraph "
        self.send_to_chatgpt() 

    # Function to check the grammar of the input paragraph
    def grammar_check(self):
        self.request="check the grammar of this paragraph" 
        self.send_to_chatgpt() 

    # Function to translate the input paragraph
    def translate(self):
        if self.target_languge.text()!="": # Check if the target language is entered
            self.request="translate this paragraph into "+self.target_languge.text() # Set the request
            self.send_to_chatgpt() 
        else:
            QMessageBox.information(self, "Error", "Target language is not entered!")


    # Function to get more information based on the input paragraph
    def more_information(self):
        self.request="give more information based on this paragraph "
        self.send_to_chatgpt() 

    # Function to propose research questions based on the input paragraph
    def get_research_question(self):
        self.request="propose research questions based on this paragraph " 
        self.send_to_chatgpt() 

    # Function to propose studies carried out in the subject of the input paragraph
    def suggest_studies(self): 
        self.request="propose studies carried out in the subject of this paragraph "
        self.send_to_chatgpt() 

    # Function to suggest references in the subject of the input paragraph
    def suggest_references(self): 
        self.request="suggest references in the subject of this paragraph " 
        self.send_to_chatgpt() 

    # Function to propose a paper title based on athe input paragraph
    def suggest_title(self): 
        self.request="propose a paper title based on this paragraph " 
        self.send_to_chatgpt()

    # Function to propose hypotheses based on the input paragraph
    def get_hypothesis(self): 
        self.request="propose hypotheses based on this paragraph " 
        self.send_to_chatgpt() 

    # Function to test the hypothesis that is in the input paragraph
    def test_hypothesis(self):
        self.request="test the hypothesis that is in this paragraph "
        self.send_to_chatgpt()

    #This function clears the output text boxe
    def clear_output(self):
        self.output_text.clear()

    #This function sets the output text as the input text
    def set_output_as_input(self):
        self.input_text.setText(self.output_text.toPlainText())
        self.output_text.clear()

    # Function to interpret results that are in the input paragraph
    def interpret_results(self):
        self.request="interpret the results that are in this paragraph "
        self.send_to_chatgpt()

    # This function is to send the paragraph as it is
    def just_send(self):
        self.request=""
        self.send_to_chatgpt()

    # This function copies the output text to the clipboard
    def copy_output(self):
        pyperclip.copy(self.output_text.toPlainText())
        QMessageBox.about(self, "Copied", "Output copied !")

    # This function sends the input text to OpenAI's GPT-3 API and displays the response in the output text box
    def send_to_chatgpt(self):
        if not self.input_text.toPlainText():
           QMessageBox.information(self, "Error", "Please provide an input text")
           return False
        try:
            question_string = self.request+'"'+self.input_text.toPlainText()+'"'
            answer = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': question_string}])
            answer_string = answer['choices'][0]['message']['content']
            self.output_text.setText(answer_string)

        except Exception as e:
            QMessageBox.information(self, "Error", f"Error encountered: {e}")

#This section creates the application instance and shows the main window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(
        app,
        theme=os.path.join(
            'style',
            'styleDark.xml'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

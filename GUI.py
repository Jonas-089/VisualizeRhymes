from PyQt5.QtWidgets import *
from calculations import *

class Window(QWidget):

    layout = QVBoxLayout()
    rhyme_array = []
    color_array = [(255, 255, 255), (255, 153, 153), (255, 204, 153), (255, 255, 153), (204, 255, 153), (153, 255, 255),
                   (153, 204, 255), (204, 153, 255), (255, 153, 255), (0, 153, 153), (127, 0, 255), (153, 51, 255),
                   (255, 128, 0), (0,255, 255), (128, 255, 0), (255, 51, 51), (204, 204, 255)]

    def __init__(self, text, rhyme_array):
        super().__init__()
        self.rhyme_array = rhyme_array
        self.setWindowTitle("rhymes")
        self.UI(text, rhyme_array)

    def UI(self, line_array, rhyme_array):

        self.setLayout(self.layout)
        self.setStyleSheet("background:rgb(255, 255, 255);")
        # self.layout.setContentsMargins(0, 0, 0, 0)

        # todo removen falls falsch
        # variable that counts the total words. Is needed because rhyme_array is not split up in lines
        consecutive_word_index = 0

        for line_index in range(len(line_array)):

            line_layout = QHBoxLayout()
            self.layout.addLayout(line_layout)

            for word_index in range(len(line_array[line_index])):

                # all syllables of a word get added as widgets (including color) to an array of widgets
                syllable_widgets = []

                syllabized_word = syllabize(line_array[line_index][word_index])

                for syllable_index in range(len(syllabized_word)):

                    syllable = syllabized_word[syllable_index]

                    syllable_widget = self.create_widget(syllable, consecutive_word_index, syllable_index)
                    syllable_widgets.append(syllable_widget)

                # add the words horizontally
                word_layout = QHBoxLayout()
                line_layout.addLayout(word_layout)

                for widget in syllable_widgets:

                    word_layout.addWidget(widget)
                    word_layout.setSpacing(0)

                consecutive_word_index += 1

        self.show()
        self.setFixedSize(self.size())

    def create_widget(self, text, word_number, vowel_number):

        widget = QLabel(text)
        widget.setStyleSheet("background:rgb" + str(self.color_array[self.rhyme_array[word_number][vowel_number]]) + ";")

        return widget

    # may not work reliably (eg.: "ocean" does not get split up)
    def syllabize(word):
        dic = pyphen.Pyphen(lang='en_US')

        syllabized_word = dic.inserted(word)

        syllabized_word_array = syllabized_word.split("-")

        return syllabized_word_array


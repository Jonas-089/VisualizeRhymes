import pronouncing
import pyphen
import sys
from GUI import *

def find_rhyming_syllables(text):

    phonetic_array = make_phonetic_array(text)

    rhyme_array = match_phones(phonetic_array)

    return rhyme_array


def make_phonetic_array(text):

    """
    returns array of the phonetics of each word in the given text
    :param text: user input
    :return: phones for the words found via the pronouncing API
    """

    word_array = text.split(" ")
    phonetic_array = []

    for word in word_array:
        if word != "\n":
            try:
                phonetic_array.append(pronouncing.phones_for_word(word)[0])
            except Exception:
                print("Error: word " + word + " not found.")

    return phonetic_array


def match_phones(phonetic_array):

    """
    matches phones of words and saves the index, relative to the words in the
    original text and relative to the position in the word itself
    :param phonetic_array:
    :return: rhyme_array
    """

    # rhyme_array gets initialized with all zeroes
    rhyme_array = build_empty_rhyme_array(phonetic_array)
    rhyme_correspondence = 1
    rhyme_found_with_current_vowel = False

    # iterates over the phonetic words
    for phone_word1_index in range(len(phonetic_array)):

        phonetic_word1_rhymes = rhyme_array[phone_word1_index]

        word1_vowels = get_vowels_of_phonetic_word(phonetic_array[phone_word1_index])

        # iterates over the vowels in the phonetic word and matches them
        for vowel1_index in range(len(word1_vowels)):

            # check next vowel if vowel was already evaluated
            if word1_vowels[vowel1_index] == "XXX":
                continue

            rhyme_found_with_current_vowel = False

            # iterates over the phonetic words that come after the first one
            for phone_word2_index in range(phone_word1_index + 1, len(phonetic_array)):

                phonetic_word2_rhymes = rhyme_array[phone_word2_index]

                # get the vowels of the current word that comes after the first word
                word2_vowels = get_vowels_of_phonetic_word(phonetic_array[phone_word2_index])

                for vowel2_index in range(len(word2_vowels)):

                    if word1_vowels[vowel1_index] == word2_vowels[vowel2_index]:

                        phonetic_word1_rhymes[vowel1_index] = rhyme_correspondence

                        phonetic_word2_rhymes[vowel2_index] = rhyme_correspondence

                        rhyme_found_with_current_vowel = True

                        # add the phonetic word rhyme arrays to the rhyme array
                        rhyme_array[phone_word1_index] = phonetic_word1_rhymes
                        rhyme_array[phone_word2_index] = phonetic_word2_rhymes

                        # deletes all vowels that are already matched so that there are no mismatchs
                        # does not work as of now
                        rhyme_array = update_rhyme_array(phonetic_array, word1_vowels[vowel1_index], rhyme_array,
                                                         rhyme_correspondence)
                        phonetic_array = update_phonetic_array(phonetic_array, word1_vowels[vowel1_index])

            if rhyme_found_with_current_vowel:
                rhyme_correspondence += 1

    return rhyme_array


def build_empty_rhyme_array(phonetic_words):
    """builds an empty rhyme array depending on the amount of vowels of each phonetic word"""

    rhyme_array = []

    for word in phonetic_words:
        rhyme_array.append([0] * len(get_vowels_of_phonetic_word(word)))

    return rhyme_array


# just like the function "get_vowels_of_word" except that it works with a phonetic word
def get_vowels_of_phonetic_word(phonetic_word):

    word_phones = phonetic_word.split(" ")

    word_vowels = []

    for phone in word_phones:
        if len(phone) == 3:
            word_vowels.append(phone)

    return word_vowels


def update_rhyme_array(phonetic_array, phone, rhyme_array, rhyme_correspondence):

    """
    updates the rhyme array so that every occurence of phone gets assigned rhyme_correspondence in the according position
    in rhyme_array
    :param phonetic_array:
    :param phone:
    :param rhyme_array:
    :param rhyme_correspondence:
    :return:
    """

    for phonetic_word_index in range(len(phonetic_array)):

        word_vowels = get_vowels_of_phonetic_word(phonetic_array[phonetic_word_index])

        for vowel_index in range(len(word_vowels)):

            if word_vowels[vowel_index] == phone:

                rhyme_array[phonetic_word_index][vowel_index] = rhyme_correspondence

    return rhyme_array


# replaces all the vowels that were already matched with dummy values
def update_phonetic_array(phonetic_array, phone):

    for phonetic_word_index in range(len(phonetic_array)):

        phonetic_array[phonetic_word_index] = phonetic_array[phonetic_word_index].replace(phone, "XXX")

    return phonetic_array


# may not work reliably (eg.: "ocean" does not get split up)
def syllabize(word):
    dic = pyphen.Pyphen(lang='en_US')

    syllabized_word = dic.inserted(word)

    syllabized_word_array = syllabized_word.split("-")

    return syllabized_word_array


def split_text_into_array(text):

    """
    preparing text for GUI by turning it into a multidimensional word array at line breaks
    :param text:
    :return: word_array
    """

    line_array = []
    word_array = []

    text_array = text.split(" ")

    for word_index in range(len(text_array)):

        if text_array[word_index] != "\n":
            line_array.append(text_array[word_index])
        else:
            word_array.append(line_array)
            line_array = []
            word_index += 1

    word_array.append(line_array)

    return word_array


def ui():

    example1 = "showing \n " \
               "glowing \n " \
               "rowing \n " \
               "knowing"

    example2 = "I went to the malls and I balled too hard \n " \
               "Oh my god, is that a black card? \n " \
               "I turned around and replied, Why yes? \n " \
               "But I prefer the term African American Express"

    text = input('Welcome to this simple rhyme analyzer. Input a simple rhyme in English or write 1 or 2 to see an example: \n')

    if text == "1":
        text = example1

    elif text == "2":
        text = example2
    else:
        pass

    text = text.replace("\\n", "\n")
    text = text.replace(".", "")
    text = text.replace(",", "")
    text = text.replace("?", "")
    text = text.replace("!", "")

    return text


def main():

    text = ui()

    rhyme_array = find_rhyming_syllables(text)

    print('Here are your rhymes:')

    print(rhyme_array)

    app = QApplication(sys.argv)
    window = Window(split_text_into_array(text), rhyme_array)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
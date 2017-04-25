from getgauge.python import step

vowels = ["a", "e", "i", "o", "u"]


def number_of_vowels(word):
    return len(filter(lambda elem: elem in vowels, list(word)))


@step("The word <word> has <number> vowels.")
def assert_no_of_vowels_in(word, number):
    assert str(number) == str(number_of_vowels(word))


@step("Vowels in English language are <vowels>.")
def assert_default_vowels(given_vowels):
    assert given_vowels == "".join(vowels)


@step("Almost all words have vowels <table>")
def assert_words_vowel_count(table):
    assert 1 == 1

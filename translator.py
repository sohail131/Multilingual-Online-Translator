import requests
from bs4 import BeautifulSoup
import sys


class MultilingualOnlineTranslator:
    def __init__(self):
        self.source_language = sys.argv[1]
        self.destination_language = sys.argv[2]
        self.word = sys.argv[3]
        self.languages_list = ("Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch",
                               "Polish", "Portuguese", "Romanian", "Russian", "Turkish")
        self.session = requests.Session()

    def mainFunction(self):
        if (self.source_language.title() not in self.languages_list) or \
                ((self.destination_language.title() not in self.languages_list) and
                 (self.destination_language != "all")):
            print("Sorry, the program doesn't support korean")
        else:
            if self.destination_language == "all":
                for i in range(0, len(self.languages_list)):
                    if i != self.source_language:
                        self.showData(destination_language=self.languages_list[i].lower())
            else:
                self.showData(destination_language=self.destination_language)

    def showData(self, destination_language):
        request = self.session.get(f"https://context.reverso.net/translation/"
                                   f"{self.source_language}-{destination_language}/{self.word}#",
                                   headers={"User-Agent": "Mozilla/5.0"})
        if request:
            soup = BeautifulSoup(request.content, "html.parser")
            soup.prettify()
            print()
            left = [i.text.strip() for i in soup.findAll("div", attrs={"class": "src ltr"})]

            if left:
                with open(f"{self.word}.txt", "a+", encoding="utf-8") as file:
                    file.write(f"{destination_language.title()} Translations:\n")
                    for i in [i.text.strip() for i in soup.find_all("a", {"class": 'translation'})][1:6]:
                        file.write(f"{i}\n")
                    file.write(f"\n{destination_language.title()} Example:\n")

                    if self.languages_list.index(destination_language.title()) == 0:
                        right = [i.text.strip() for i in soup.find_all("div", attrs={"class": "trg rtl arabic"})]
                    elif self.languages_list.index(destination_language.title()) == 5:
                        right = [i.text.strip() for i in soup.find_all("div", attrs={"class": "trg rtl"})]
                    else:
                        right = [i.text.strip() for i in soup.find_all("div", attrs={"class": "trg ltr"})]
                    for l, j, k in zip(range(5), left, right):
                        file.write(f"{j}\n{k}\n")

                with open(f"{self.word}.txt", "r", encoding="utf-8") as file:
                    for i in file.read().split("\n"):
                        print(i)
            else:
                print(f"Sorry, unable to find {self.word}")
        else:
            print("Something wrong with your internet connection")


if __name__ == '__main__':
    MultilingualOnlineTranslator().mainFunction()

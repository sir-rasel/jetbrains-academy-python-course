from bs4 import BeautifulSoup
import requests
import sys


class Translator:
    def __init__(self):
        self.languages = (
            'Arabic', 'German', 'English', 'Spanish', 'French',
            'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
            'Romanian', 'Russian', 'Turkish'
        )
        self.lang_src, self.lang_tgt = None, tuple()
        self.word = None
        self.response = None
        self.translations = tuple()
        self.examples_src, self.examples_tgt = tuple(), tuple()
        self.examples_paired = tuple(tuple())
        self.url = 'https://context.reverso.net/translation'
        self.output_file = None

    def main(self):
        if len(sys.argv) > 1:
            self.inline_request()
        else:
            self.welcome_message()
            
        self.request_translation()
        self.display_results()
        
    def inline_request(self):
        args = tuple(arg.title() for arg in sys.argv)
        
        try:
            self.lang_src, self.lang_tgt = args[1], tuple(args[2:-1])
            self.word = args[-1]
        except IndexError:
            sys.exit('Insufficient number of arguments provided. Please try again.')
        else:
            if args[2] == 'All':
                self.lang_tgt = tuple(lang for lang in self.languages if lang not in (self.lang_src))
        
    def welcome_message(self):
        print("Hello! I am the Translator. I currently support:")
        for i, lang in enumerate(self.languages):
            print(f'{i+1}. {self.languages[i]}')
            
        option_lang_src = input('Select language to translate from: ')
        self.lang_src = self.languages[int(option_lang_src)-1]
        option_lang_tgt = input("Select language to translate to ('0' for all languages): ")
        self.lang_tgt = (self.languages[int(option_lang_tgt)-1],) if option_lang_tgt != '0' \
            else (lang for lang in self.languages if lang not in (self.lang_src))
        self.word = input('Type the word you want to translate: ')
            
    def request_translation(self):
        self.output_file = open(self.word.lower() + '.txt', 'w+')

        for lang in self.lang_tgt:
            if lang not in self.languages:
                print(f"Sorry the program doesn't support {lang}")
                if len(self.lang_tgt) == 1:
                    sys.exit()
                else:
                    continue
        
            url = self.url + f'/{self.lang_src.lower()}-{lang.lower()}/{self.word.lower()}'
            self.response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            if self.response:
                soup = BeautifulSoup(self.response.content, 'html.parser')
                self.translations = tuple(transl.get_text(strip=True) for transl
                                     in soup.select('#translations-content > .translation')[:5])
                self.examples_src = tuple(example.get_text(strip=True) for example
                                     in soup.select('#examples-content > .example > .src')[:5])
                self.examples_tgt = tuple(example.get_text(strip=True) for example
                                     in soup.select('#examples-content > .example > .trg')[:5])
                self.examples_paired = tuple((src, tgt) for src, tgt in zip(self.examples_src, self.examples_tgt))
            elif self.response.status_code == 404:
                print(f'Sorry, unable to find {self.word.lower()}')
                sys.exit()
            else:
                sys.exit('Something wrong with your internet connection')

            self.print_to_file(lang)
            
    def print_to_file(self, lang):
        self.output_file.write(f'{lang} Translations\n')
        self.output_file.writelines('\n'.join(self.translations))
        self.output_file.write(f'{lang} Examples\n')
        self.output_file.write('\n'.join(tuple(f'{src}\n{tgt}' for (src, tgt) in self.examples_paired)))
        self.output_file.write('\n')
            
    def display_results(self):
        self.output_file.seek(0)
        print('\n' + self.output_file.read())
        self.output_file.close()


if __name__ == '__main__':
    translator = Translator()
    translator.main()

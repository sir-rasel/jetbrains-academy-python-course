class RegexEngine:
    def __init__(self, regex, string):
        self.regex = regex
        self.string = string

    def __str__(self):
        return str(self.check_is_regex_matched_string(self.regex, self.string))

    def check_single_charecter_matched(self, regex, input):
        if regex == '' or regex == '.' or regex == input:
            return True
        return False


    def check_matched(self, regex, input):
        if regex == '':
            return True
        if regex == '$' and input == '':
            return True
        if input == '':
            return False
        if len(regex) > 1:
            if regex[0] == '\\':
                if self.check_single_charecter_matched(regex[1], input[0]) is True:
                    return self.check_matched(regex[2:], input[1:])
                else:
                    return False
            if (regex[1] == '?' or regex[1] == '*') and self.check_single_charecter_matched(regex[0], input[0]) is False:
                return self.check_matched(regex[2:], input)
            if regex[1] == '?' and self.check_single_charecter_matched(regex[0], input[0]) is True:
                return self.check_matched(regex[2:], input[1:])
            if regex[1] == '*' or regex[1] == '+':
                i = 0
                while self.check_single_charecter_matched(regex[0], input[i]) is True:
                    i += 1
                    if i >= len(input) or input[i] != input[i-1]:
                        break
                if i > 0:
                    return self.check_matched(regex[2:], input[i:])
        if self.check_single_charecter_matched(regex[0], input[0]) is False:
            return False
        return self.check_matched(regex[1:], input[1:])


    def check_is_regex_matched_string(self, regex, input):
        if regex == '':
            return True
        if regex[0] == '^':
            return self.check_matched(regex[1:], input)
        for i in range(len(input)):
            if self.check_matched(regex, input[i:]) is True:
                return True
        return False

def main():
    regex, string = input().split('|')
    matching_engine = RegexEngine(regex, string)

    print(matching_engine)

if __name__ == "__main__":
    main()
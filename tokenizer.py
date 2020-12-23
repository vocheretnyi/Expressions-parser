import re


class Token:
    def __init__(self, text, index):
        self.text = text
        self.index = index
        if text == 'x':
            self.kind = 'variable'
        elif re.match(r"[0-9]+(\.[0-9]*)?([eE][+-]?[0-9]+)?", text):
            self.kind = 'number'
        elif re.match(r"PI|E", text):
            self.kind = 'constant'
        elif re.match(r"[*+-/^()@,]", text):
            self.kind = 'operator'
        else:
            self.kind = 'function'

    def __str__(self):
        return self.text


class Tokenizer:
    @staticmethod
    def tokenize(text):
        text_len = len(text)
        token_list = []
        token_pattern = r"[0-9]+(\.[0-9]*)?([eE][\+\-]?[0-9]+)?|[a-zA-Z]+|[*+-\/(),]"
        while True:
            match = re.match(token_pattern, text)
            if re.match(r'[a-zA-Z]+', text) and not re.match(r'x|sin|cos|tg|pow|exp|abs|sqrt|E|PI', text):
                raise BaseException(f'Unknown function {match.group(0)} detected at position {text_len - len(text)}')
            if not match:
                if len(text.strip()) > 0:
                    raise BaseException(
                        f'Unknown symbol {text[0]} detected at position {text_len - len(text) + 1}')
                break
            new_token = Token(match.group(0), text_len - len(text))
            if new_token.kind == 'operator' and new_token.text == '-' \
                    and (len(token_list) == 0 or (token_list[-1].kind == 'operator'
                         and token_list[-1].text != ')')):
                new_token = Token('@', text_len - len(text))
            token_list.append(new_token)
            text = text[match.start() + len(match.group(0)):]
        return token_list

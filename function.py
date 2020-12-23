from tokenizer import Tokenizer
import math


class Function:
    def __init__(self, formula):
        self.tokens = Tokenizer.tokenize(formula)
        self.rpn = []
        self.precedence = {
            '@': 9,
            '*': 8,
            '/': 8,
            '+': 6,
            '-': 6,
            '(': -1,
        }
        self.constants = {
            'PI': math.pi,
            'E': math.e
        }

    def calc(self, val):
        self.rpn = []
        out = []
        ops = []
        for token in self.tokens:
            if token.kind == 'number':
                out.append(float(token.text))
                self.rpn.append(token)
            elif token.kind == 'variable':
                out.append(val)
                self.rpn.append(token)
            elif token.kind == 'constant':
                out.append(self.constants[token.text])
                self.rpn.append(token)
            elif token.kind == 'function':
                ops.append(token)
            elif token.text == '(':
                ops.append(token)
            elif token.text == ')':
                while len(ops) > 0:
                    if ops[-1].text == '(':
                        ops.pop()
                        break
                    else:
                        self.rpn.append(ops[-1])
                        self.apply_operation(ops.pop(), out)
                else:
                    raise BaseException(f'Opening parenthesis is missing for \')\' at position {token.index}')
            else:
                while len(ops) > 0 and (ops[-1].kind == 'function' or
                                        self.precedence[ops[-1].text] >= self.precedence[token.text]):
                    self.rpn.append(ops[-1])
                    self.apply_operation(ops.pop(), out)
                ops.append(token)
        while len(ops) > 0:
            token = ops.pop()
            if token.text == '(':
                raise BaseException(f'Closing parenthesis is missing for \'(\' at position {token.index}')
            self.rpn.append(token)
            self.apply_operation(token, out)
        if len(out) > 1:
            raise BaseException(f'Too many numbers in the expression')
        return out[0]

    def apply_operation(self, token, out):
        operation = token.text
        try:
            if operation == '@':
                out.append(-out.pop())
            if operation == '+':
                out.append(out.pop() + out.pop())
            if operation == '-':
                op1 = out.pop()
                op2 = out.pop()
                out.append(op2 - op1)
            if operation == '*':
                out.append(out.pop() * out.pop())
            if operation == '/':
                op1 = out.pop()
                op2 = out.pop()
                out.append(op2 / op1)
            if operation == 'pow':
                op1 = out.pop()
                op2 = out.pop()
                out.append(op2 ** op1)
            if operation == 'sin':
                out.append(math.sin(out.pop()))
            if operation == 'cos':
                out.append(math.cos(out.pop()))
            if operation == 'tg':
                out.append(math.tan(out.pop()))
            if operation == 'abs':
                out.append(abs(out.pop()))
            if operation == 'sqrt':
                out.append(math.sqrt(out.pop()))
            if operation == 'exp':
                out.append(math.e ** out.pop())
        except:
            raise BaseException(f'Invalid number of arguments for {operation} at position {token.index}')

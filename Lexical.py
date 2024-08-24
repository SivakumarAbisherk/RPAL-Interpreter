class TokenType:
    EQ = "EQ"
    IN = "IN"
    GR = "GR"
    GE = "GE"
    LS = "LS"
    LE = "LE"
    EQUALS = "EQUALS"
    NE = "NE"
    OR = "OR"
    FN = "FN"
    LET = "LET"
    NOT = "NOT"
    NEG = "NEG"
    NIL = "NIL"
    AND = "AND"
    REC = "REC"
    AUG = "AUG"
    TRUE = "TRUE"
    FALSE = "FALSE"
    WHERE = "WHERE"
    DUMMY = "DUMMY"
    WITHIN = "WITHIN"
    ID = "ID"
    INTEGER = "INTEGER"
    STRING = "STRING"
    L_PAREN = "L_PAREN"
    R_PAREN = "R_PAREN"
    SEMI = "SEMI"
    COMMA = "COMMA"
    PERIOD = "PERIOD"
    AND_BIN = "AND_BIN"
    TIMES = "TIMES"
    PLUS = "PLUS"
    MINUS = "MINUS"
    DIVIDE = "DIVIDE"
    AT = "AT"
    BAR = "BAR"
    OP = "OP"
    CONDITIONAL = "CONDITIONAL"
    EXPO = "EXPO"
    EOF = "EOF"

class Token:
    def __init__(self, type, value, length, line_num):
        self.type = type
        self.name = value
        self.length = length
        self.location = line_num

class Result:
    def __init__(self, success, token):
        self.success = success
        self.token = token

class Lexer:
    def __init__(self, file_name):
        try:
            self.file = open(file_name, "r")
        except IOError as e:
            print("Error opening file:", e)
            exit(1)

        self.current_line = self.file.readline()
        if not self.current_line:
            print("File is empty.")
            exit(1)
        
        self.cur_line_num = 1
        self.cur_idx = 0

    def is_valid_escape_char(self, char1, char2):
        if char1 == '\\' and char2 in ['\\', '\'', 't', 'n']:
            return True
        return False

    def is_operator(self, test_char):
        operators = "'\"+-*<>&.@/:=~|$!#%^_[]{}`?"
        if test_char in operators:
            return True
        return False

    def is_space(self, test_char):
        return test_char.isspace()

    def is_alphabet(self, ch):
        return ch.isalpha()

    def get_identifier_type(self, test_string):
        # Define identifier types here
        identifier_types = {
            "in": TokenType.IN,
            "gr": TokenType.GR,
            "ge": TokenType.GE,
            "ls": TokenType.LS,
            "le": TokenType.LE,
            "eq": TokenType.EQ,
            "ne": TokenType.NE,
            "or": TokenType.OR,
            "fn": TokenType.FN,
            "let": TokenType.LET,
            "not": TokenType.NOT,
            "neg": TokenType.NEG,
            "nil": TokenType.NIL,
            "and": TokenType.AND,
            "rec": TokenType.REC,
            "aug": TokenType.AUG,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "where": TokenType.WHERE,
            "dummy": TokenType.DUMMY,
            "within": TokenType.WITHIN
        }
        return identifier_types.get(test_string, TokenType.ID)

    def make_identifier(self, test_string):
        prev_idx = self.cur_idx
        i = self.cur_idx
        if self.is_alphabet(test_string[i]):
            while i < len(test_string) and (test_string[i].isdigit() or self.is_alphabet(test_string[i]) or test_string[i] == '_'):
                i += 1
            test_token = test_string[prev_idx:i]
            self.cur_idx = i
            return Result(True, Token(self.get_identifier_type(test_token), test_token, len(test_token), self.cur_line_num))
        return Result(False, None)

    def make_string(self, test_string):
        prev_idx = self.cur_idx
        i = self.cur_idx
        if test_string[i] == '\'':
            i += 1
            while i < len(test_string) and test_string[i] != '\'':
                if test_string[i] == '\\' and i + 1 < len(test_string):
                    i += 2
                else:
                    i += 1
            if i < len(test_string) and test_string[i] == '\'':
                test_token = test_string[prev_idx + 1:i]
                self.cur_idx = i + 1
                return Result(True, Token(TokenType.STRING, test_token, len(test_token), self.cur_line_num))
        return Result(False, None)

    def make_comment(self, test_string):
        if test_string.startswith("//"):
            return True
        return False

    def make_integer(self, test_string):
        prev_idx = self.cur_idx
        i = self.cur_idx
        if test_string[i].isdigit():
            while i < len(test_string) and test_string[i].isdigit():
                i += 1
            test_token = test_string[prev_idx:i]
            self.cur_idx = i
            return Result(True, Token(TokenType.INTEGER, test_token, len(test_token), self.cur_line_num))
        return Result(False, None)

    def make_delimiter(self, test_string):
        delimiters = {'(': TokenType.L_PAREN, ')': TokenType.R_PAREN, ';': TokenType.SEMI, ',': TokenType.COMMA}
        if test_string[self.cur_idx] in delimiters:
            ch = test_string[self.cur_idx]
            self.cur_idx += 1
            return Result(True, Token(delimiters[ch], ch, 1, self.cur_line_num))
        return Result(False, None)

    def get_reserved_operators_type(self, operator):
        operator_types = {
            '.': TokenType.PERIOD,
            '&': TokenType.AND_BIN,
            '*': TokenType.TIMES,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '/': TokenType.DIVIDE,
            '@': TokenType.AT,
            '|': TokenType.BAR,
            '=': TokenType.EQUALS,
            '->':TokenType.CONDITIONAL
        }
        return operator_types.get(operator, TokenType.OP)

    def make_operator(self, test_string):
        i = self.cur_idx
        if self.is_operator(test_string[i]):
            if test_string[i:i + 2] in ['>=', '<=', '->', '**']:
                self.cur_idx += 2
                operator = test_string[i:i + 2]
                return Result(True, Token(self.get_reserved_operators_type(operator), operator, 2, self.cur_line_num))
            else:
                self.cur_idx += 1
                operator = test_string[i]
                return Result(True, Token(self.get_reserved_operators_type(operator), operator, 1, self.cur_line_num))
        return Result(False, None)

    def scan(self):
        while self.cur_idx < len(self.current_line) and self.current_line[self.cur_idx].isspace():
            self.cur_idx += 1

        if self.cur_idx >= len(self.current_line):
            self.current_line = self.file.readline()
            if not self.current_line:
                return Token(TokenType.EOF, "EOF", 3, self.cur_line_num)
            self.cur_line_num += 1
            self.cur_idx = 0

        if self.cur_idx >= len(self.current_line):
            self.cur_line_num += 1
            self.current_line = self.file.readline()
            if not self.current_line:
                return Token(TokenType.EOF, "EOF", 3, self.cur_line_num)
            self.cur_idx = 0

        if self.cur_idx >= len(self.current_line):
            return Token(TokenType.EOF, "EOF", 3, self.cur_line_num)

        if self.make_comment(self.current_line):
            self.current_line = self.file.readline()
            self.cur_line_num += 1
            self.cur_idx = 0
            return self.scan()

        result = self.make_identifier(self.current_line)
        if result.success:
            return result.token

        result = self.make_string(self.current_line)
        if result.success:
            return result.token

        result = self.make_operator(self.current_line)
        if result.success:
            return result.token

        result = self.make_integer(self.current_line)
        if result.success:
            return result.token

        result = self.make_delimiter(self.current_line)
        if result.success:
            return result.token

        # If none of the above, advance the index and rescan
        self.cur_idx += 1
        return self.scan()

def main():
    file_name = "input.txt"
    lexer = Lexer(file_name)

    try:
        while True:
            token = lexer.scan()
            if token.type == TokenType.EOF:
                break
            print(f"Token: {token.type}, Value: {token.name}, Length: {token.length}, Line Number: {token.location}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

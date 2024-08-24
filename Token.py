class Token:
    def __init__(self, typ=None, name=None, length=None, location=None):
        self.type = typ
        self.name = name
        self.length = length  # the length of token
        self.location = location  # the line number of the token in the file

    def print_token_attributes(self):
        print(f"{self.type}\t{self.name}\t{self.length}\t{self.location}")


class TokenType:
    EQ= "EQ"
    ID = "ID"
    INTEGER = "INTEGER"
    STRING = "STRING"
    EOF = "EOF"
    L_PAREN = "L_PAREN"
    R_PAREN = "R_PAREN"
    SEMI = "SEMI"
    COMMA = "COMMA"
    IN = "IN"
    GR = "GR"
    GE = "GE"
    LS = "LS"
    LE = "LE"
    NE = "NE"
    OR = "OR"
    FN = "FN"
    AT = "AT"
    OP = "OP"  # for any of these: '\"+-*<>&.@/:=~|$!#%^_[]{}`?
    LET = "LET"
    NOT = "NOT"
    NEG = "NEG"
    NIL = "NIL"
    AND = "AND"
    AND_BIN = "AND_BIN"
    REC = "REC"
    AUG = "AUG"
    BAR = "BAR"
    EXPO = "EXPO"
    TRUE = "TRUE"
    PLUS = "PLUS"
    WHERE = "WHERE"
    FALSE = "FALSE"
    DUMMY = "DUMMY"
    TIMES = "TIMES"
    MINUS = "MINUS"
    WITHIN = "WITHIN"
    PERIOD = "PERIOD"
    DIVIDE = "DIVIDE"
    EQUALS = "EQUALS"
    CONDITIONAL = "CONDITIONAL"
    ERROR = "ERROR"  # not possible: just to check for error
    FUNCTION_FORM = "FUNCTION_FORM"
    GAMMA = "GAMMA"
    TAU = "TAU"
    LAMBDA = "LAMBDA"
    YSTAR = "YSTAR"  # new tokenTypes: only for tree construction
    # define types here

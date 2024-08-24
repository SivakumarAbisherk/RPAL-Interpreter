import sys

from CSEMachine import CSEMachine
from ControlStructure import ControlStructureGenerator
from Lexical import Lexer
from Treebuilder import TreeBuilder, Node
from Token import Token
from Token import TokenType


class Parser:
    def __init__(self, file_name):
        self.next_token = None
        self.lexer = None
        self.tree_builder = None
        try:
            self.lexer = Lexer(file_name)
            self.next_token = self.lexer.scan()
            self.tree_builder = TreeBuilder()
        except IOError:
            sys.exit(1)

    def get_tree_builder(self):
        return self.tree_builder

    def read(self, token):
        if (token.type == TokenType.ID) or (token.type == TokenType.INTEGER) or (token.type == TokenType.STRING):
            self.tree_builder.build_tree(token, 0)
        try:
            self.next_token = self.lexer.scan()
            if self.next_token.type == TokenType.EOF:
                return
        except IOError:
            print(" !!!!!! error !!!!! ")

    def parse_error(self, token_name, found_token):
        print("Expected token '" + token_name + "' but found '" + found_token.name + "' on line num " + str(found_token.location))
        sys.exit(1)

    def start_parsing(self):
        self.E()


#  Expressions ############################################
	#  E ->'let' D 'in' E => 'let'
	#   ->'fn' Vb+ '.' E => 'lambda'
	#   ->Ew;

    def E(self):
        if self.next_token.type == TokenType.LET:
            # print("* E ->'let' D 'in' E ")
            let_token = self.next_token
            self.read(self.next_token)
            self.D()
            if self.next_token.type != TokenType.IN:
                self.parse_error("in", self.next_token)
            self.read(self.next_token)
            self.E()
            self.tree_builder.build_tree(let_token, 2)
        elif self.next_token.type == TokenType.FN:
            # print("E->'fn' Vb+ '.' E ")
            lambda_token = Token(TokenType.LAMBDA, "lambda")
            self.read(self.next_token)
            n = 0
            self.Vb()
            while (self.next_token.type == TokenType.ID) or (self.next_token.type == TokenType.L_PAREN):
                self.Vb()
                n += 1
            if not (self.next_token.name == "."):
                self.parse_error(".", self.next_token)
            self.read(self.next_token)
            self.E()
            self.tree_builder.build_tree(lambda_token, n + 2)
        else:
            # print("E->Ew")
            self.Ew()


# Ew ->T 'where' Dr => 'where'
# 	 ->T;

    def Ew(self):
        self.T()
        if self.next_token.type == TokenType.WHERE:
            # print("Ew ->T 'where' Dr")
            where_token = self.next_token
            self.read(self.next_token)
            self.Dr()
            self.tree_builder.build_tree(where_token, 2)
        # else:
        #     print("Ew->T")


#   T -> Ta ( ',' Ta )+ => 'tau'
# 	  -> Ta ;

    def T(self):
        self.Ta()
        if self.next_token.type == TokenType.COMMA:
            # print("T -> Ta ( ',' Ta )+")
            tau_token = Token(TokenType.TAU, "tau")
            n = 0
            while self.next_token.type == TokenType.COMMA:
                self.read(self.next_token)
                self.Ta()
                n += 1
            self.tree_builder.build_tree(tau_token, n + 1)
        # else:
        #     print("T -> Ta")


#  Ta -> Ta 'aug' Tc => 'aug'
# 	 -> Tc ;

    def Ta(self):
        self.Tc()
        # if self.next_token.type == TokenType.AUG:
            # print("Ta -> Ta 'aug' Tc")
        while self.next_token.type == TokenType.AUG:
            aug_token = self.next_token
            self.read(self.next_token)
            self.Tc()
            self.tree_builder.build_tree(aug_token, 2)
        # else:
        #     print("Ta-> Tc")


#   Tc -> B '->' Tc '|' Tc => '->'
#     -> B ;

    def Tc(self):
        self.B()
        if self.next_token.type == TokenType.CONDITIONAL:
            # print("Tc -> B '->' Tc '|' Tc ")
            cond_token = self.next_token
            self.read(self.next_token)
            self.Tc()
            if self.next_token.type != TokenType.BAR:
                self.parse_error("|", self.next_token)
            self.read(self.next_token)
            self.Tc()
            self.tree_builder.build_tree(cond_token, 3)
        # else:
        #     print("Tc-> B")

# Boolean Expressions ####################################
# 	 * B -> B 'or' Bt => 'or'
# 	 * -> Bt ;


    def B(self):
        self.Bt()
        while self.next_token.type == TokenType.OR:
            or_token = self.next_token
            self.read(self.next_token)
            self.Bt()
            self.tree_builder.build_tree(or_token, 2)


# * Bt -> Bt '&' Bs => '&'
# 	 * -> Bs ;

    def Bt(self):
        self.Bs()
        while self.next_token.type == TokenType.AND_BIN:
            and_token = self.next_token
            self.read(self.next_token)
            self.Bs()
            self.tree_builder.build_tree(and_token, 2)


# * Bs -> 'not' Bp => 'not'
# 	 * -> Bp ;

    def Bs(self):
        if self.next_token.type == TokenType.NOT:
            not_token = self.next_token
            self.read(self.next_token)
            self.Bp()
            self.tree_builder.build_tree(not_token, 1)
        else:
            self.Bp()



    def Bp_helper(self, token):
        self.read(self.next_token)
        self.A()
        self.tree_builder.build_tree(token, 2)


	#  * Bp -> A ('gr' | '>' ) A => 'gr'
	#  * -> A ('ge' | '>=') A => 'ge'
	#  * -> A ('ls' | '<' ) A => 'ls'
	#  * -> A ('le' | '<=') A => 'le'
	#  * -> A 'eq' A => 'eq'
	#  * -> A 'ne' A => 'ne'
	#  * -> A ;

    def Bp(self):
        self.A()
        if self.next_token.name in ["gr", ">", "ge", ">=", "ls", "<", "le", "<=", "eq", "ne"]:
            self.Bp_helper(self.next_token)


#  Arithmetic Expressions #################################
#   A -> A '+' At => '+'
# 	  -> A '-' At => '-'
# 	  -> '+' At
# 	  -> '-'At =>'neg'
# 	  -> At ;

    def A(self):
        if self.next_token.name == "+":
            self.read(self.next_token)
            self.At()
        elif self.next_token.name == "-":
            neg_token = Token(TokenType.NEG, "neg")
            self.read(self.next_token)
            self.At()
            self.tree_builder.build_tree(neg_token, 1)
        else:
            self.At()
        while self.next_token.name in ["+", "-"]:
            current_token = self.next_token
            self.read(self.next_token)
            self.At()
            self.tree_builder.build_tree(current_token, 2)


#  At -> At '*' Af => '*'
# 	  -> At '/' Af => '/'
# 	  -> Af ;

    def At(self):
        self.Af()
        while self.next_token.name in ["*", "/"]:
            current_token = self.next_token
            self.read(self.next_token)
            self.Af()
            self.tree_builder.build_tree(current_token, 2)


#  Af -> Ap '**' Af => '**'
# 	  -> Ap ;

    def Af(self):
        self.Ap()
        while self.next_token.name == "**":
            exp_token = self.next_token
            self.read(self.next_token)
            self.Af()
            self.tree_builder.build_tree(exp_token, 2)


# Ap -> Ap '@' '<IDENTIFIER>' R => '@'
# 	  -> R ;

    def Ap(self):
        self.R()
        while self.next_token.name == "@":
            at_token = self.next_token
            self.read(self.next_token)
            if self.next_token.type != TokenType.ID:
                self.parse_error("ID", self.next_token)
            self.read(self.next_token)
            self.R()
            self.tree_builder.build_tree(at_token, 3)

# Rators And Rands #######################################
	#  * R -> R Rn => 'gamma'
	#  * -> Rn ;
	#  */

    def R(self):
        if self.Rn():
            while self.Rn():
                gamma_token = Token(TokenType.GAMMA, "gamma")
                self.tree_builder.build_tree(gamma_token, 2)


	#  * Rn -> '<IDENTIFIER>'
	#  * -> '<INTEGER>'
	#  * -> '<STRING>'
	#  * -> 'true' => 'true'
	#  * -> 'false' => 'false'
	#  * -> 'nil' => 'nil'
	#  * -> '(' E ')'
	#  * -> 'dummy' => 'dummy' ;
	#  */

    def Rn(self):
        if self.next_token.type in [TokenType.ID, TokenType.INTEGER, TokenType.STRING, TokenType.TRUE, TokenType.FALSE,
                                    TokenType.NIL, TokenType.L_PAREN, TokenType.DUMMY]:
            if self.next_token.type in [TokenType.ID, TokenType.INTEGER, TokenType.STRING]:
                self.read(self.next_token)
                return True
            elif self.next_token.type in [TokenType.TRUE, TokenType.FALSE, TokenType.NIL, TokenType.DUMMY]:
                current_token = self.next_token
                self.read(self.next_token)
                self.tree_builder.build_tree(current_token, 0)
                return True
            elif self.next_token.type == TokenType.L_PAREN:
                self.read(self.next_token)
                self.E()
                if self.next_token.type != TokenType.R_PAREN:
                    self.parse_error(")", self.next_token)
                self.read(self.next_token)
                return True
        elif self.next_token.type == TokenType.REC:
            self.read(self.next_token)
            self.Dr()
            return True
        return False
    
    
 # Definitions ############################################
# 	  D -> Da 'within' D => 'within'
# 	    -> Da ;

    def D(self):
        # print("D -> Da")
        self.Da()
        if self.next_token.type == TokenType.WITHIN:
            print("D -> Da 'within' D")
            within_token = self.next_token
            self.read(self.next_token)
            self.D()
            self.tree_builder.build_tree(within_token, 2)


#  Da -> Dr ( 'and' Dr )+ => 'and'
# 	  -> Dr ;

    def Da(self):
        # print("Da -> Dr")
        self.Dr()
        if self.next_token.type == TokenType.AND:
            # print("Da -> Dr ( 'and' Dr )+")
            and_token = self.next_token
            n = 0
            while self.next_token.type == TokenType.AND:
                self.read(self.next_token)
                self.Da()
                n += 1
            self.tree_builder.build_tree(and_token, n + 1)


# * Dr -> 'rec' Db => 'rec'
# 	 * -> Db ;

    def Dr(self):
        if self.next_token.type == TokenType.REC:
            # print("Dr -> 'rec' Db => 'rec'")
            rec_token = self.next_token
            self.read(self.next_token)
            self.Db()
            self.tree_builder.build_tree(rec_token, 1)
        else:
            # print("Dr-> Db ")
            self.Db()

# * Db -> Vl '=' E => '='
# 	 * -> '<IDENTIFIER>' Vb+ '=' E => 'fcn_form'
# 	 * -> '(' D ')' ;

    def Db(self):
        if self.Vl():
            if self.next_token.type == TokenType.EQUALS:
                # print("Db -> Vl '=' E")
                eq_token = self.next_token
                self.read(self.next_token)
                self.E()
                self.tree_builder.build_tree(eq_token, 2)  # =
                return
            else:
                # print("Db-> '<IDENTIFIER>' Vb+ '=' E")
                n = 0
                while self.next_token.type == TokenType.ID or self.next_token.type == TokenType.L_PAREN:
                    self.Vb()
                    n += 1
                if self.next_token.type != TokenType.EQUALS:
                    self.parse_error("=", self.next_token)
                self.read(self.next_token)
                self.E()
                function_form_token = Token(TokenType.FUNCTION_FORM, "function_form")
                self.tree_builder.build_tree(function_form_token, n + 2)
        elif self.next_token.type == TokenType.L_PAREN:
            # print("-> '(' D ')' ")
            self.read(self.next_token)
            self.D()
            if self.next_token.type != TokenType.R_PAREN:
                self.parse_error(")", self.next_token)
            self.read(self.next_token)
        else:
            self.parse_error("( Left Parenthesis OR ID ", self.next_token)


# Variables ##############################################
	#  * Vb -> '<IDENTIFIER>'
	#  * -> '(' Vl ')'
	#  * -> '(' ')' => '()';

    def Vb(self):
        if self.next_token.type == TokenType.ID:
            # print(" Vb -> '<IDENTIFIER>'")
            self.read(self.next_token)
        elif self.next_token.type == TokenType.L_PAREN:
            self.read(self.next_token)
            if self.next_token.type == TokenType.ID:
                # print("Vb -> '(' Vl ')'")
                self.Vl()
                if self.next_token.type != TokenType.R_PAREN:
                    self.parse_error(")", self.next_token)
                self.read(self.next_token)
            elif self.next_token.type == TokenType.R_PAREN:
                # print("Vb -> '(' ')'")
                rparen_token = self.next_token
                self.read(self.next_token)
                self.tree_builder.build_tree(rparen_token, 2)  # be careful about this while printing AST
            else:
                self.parse_error("ID or )", self.next_token)
        else:
            self.parse_error("Left Parenthesis OR ID", self.next_token)

# Vl -> '<IDENTIFIER>' list ',' => ','?;

    def Vl(self):
        n = 1
        comma_token = Token()
        if self.next_token.type == TokenType.ID:
            self.read(self.next_token)
            if self.next_token.type == TokenType.COMMA:
                comma_token = self.next_token
                while self.next_token.type == TokenType.COMMA:
                    self.read(self.next_token)
                    n += 1
                    if self.next_token.type != TokenType.ID:
                        self.parse_error("ID", self.next_token)
                    self.read(self.next_token)
        if n == 1:
            return True
        if n > 1:
            self.tree_builder.build_tree(comma_token, n)  # ,
            return True
        return False


def test_parser(input_file , is_print_ast, is_print_st):
    # Create a Parser instance with the input file
    parser = Parser("input.txt")

    # Start parsing
    parser.start_parsing()

    # Get the tree builder to retrieve the AST
    tree_builder = parser.get_tree_builder()
    root = tree_builder.stack.pop()
    # Print the AST
    if is_print_ast:
        if root is None:
            print("!!!!!ERROR in PrintTree()!!!")
        tree_builder.preorder(root, 0)
    # tree_builder.print_tree()



    standarizer=Node(Token(TokenType.ID,"standarizer"))

    root=standarizer.standarize(root)
    if is_print_st:
        tree_builder.print_tree()
    # tree_builder.preorder(root, 0)
    ctrlStructGen = ControlStructureGenerator()
    ctr_structures = ctrlStructGen.generate_control_structures(root)
    # ctrlStructGen.print_ctrl_structs()
    if is_print_st == False and is_print_ast == False:
        # ctrlStructGen.print_ctrl_structs()
        cseMachine = CSEMachine(ctr_structures, "input.txt")
        result = cseMachine.execute()




    # root = tree_builder.stack.pop()
    # root.standarize()


# Run the test case
# test_parser()

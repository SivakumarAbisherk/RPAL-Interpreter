from Token import TokenType
import Token
class Node:
    def __init__(self, token):
        self.token = token
        self.first = None
        self.sibling = None
        self.previous = None

    def createCopy (self):
        node = Node( Token.Token( self.token.type, self.token.name))
        node.value = self.token.name
        # node.sourceLineNumber = self.token.sourceLineNumber
        node.first = self.first
        node.sibling = self.sibling
        node.previous = self.previous
        return node

    def standarize(self, root):

        if root == None:
            return None


        root.first = self.standarize(root.first)

        if root.sibling != None:
            root.sibling = self.standarize(root.sibling)

        nextSibling = root.sibling

        # prevSibling = root.previous
        # nextSibling = root.sibling

        match root.token.type:
            case Token.TokenType.LET:
                #print("let")
                #print( "type : " , root.first.type)
                if root.first.token.type == Token.TokenType.EQUALS:
                    #print("equal")
                    equal = root.first
                    P = equal.sibling
                    X = equal.first
                    E = X.sibling
                    lambdaNode = Node( Token.Token(Token.TokenType.LAMBDA, "lambda"))
                    gammaNode = Node(Token.Token(Token.TokenType.GAMMA, "gamma"))
                    gammaNode.first = lambdaNode
                    lambdaNode.sibling = E
                    #print("stantdarizing let #######")
                    X.sibling = P
                    lambdaNode.first = X







                    # P.previous = X
                    gammaNode.sibling = nextSibling


                    return gammaNode
                else:
                    root.sibling = nextSibling

                    return root

            case Token.TokenType.WHERE:
                if root.first.sibling.token.type== Token.TokenType.EQUALS:
                    P = root.first
                    equal = P.sibling
                    X = equal.first
                    E = X.sibling
                    lambdaNode = Node( Token.Token(Token.TokenType.LAMBDA, "lambda"))
                    gammaNode = Node(Token.Token(Token.TokenType.GAMMA, "gamma"))

                    gammaNode.first = lambdaNode
                    lambdaNode.sibling = E
                    lambdaNode.first = X

                    X.sibling = P
                    # P.previous = gammaNode
                    P.sibling = None

                    gammaNode.sibling = nextSibling


                    return gammaNode
                else:
                    root.sibling = nextSibling

                    return root

            case Token.TokenType.FUNCTION_FORM:
                P = root.first
                V = P.sibling
                Vs = V.sibling

                newRoot = Node(Token.Token(Token.TokenType.EQUALS, "="))
                newRoot.first = P

                lambdaNode = Node(Token.Token(Token.TokenType.LAMBDA, "lambda"))
                P.sibling = lambdaNode
                lambdaNode.previous = P

                while Vs.sibling != None:
                    lambdaNode.first = V
                    lambdaNode = Node(Token.Token(Token.TokenType.LAMBDA, "lambda"))
                    V.sibling = lambdaNode
                    lambdaNode.previous = V
                    V = Vs
                    Vs = Vs.sibling

                lambdaNode.first = V
                V.sibling = Vs
                Vs.previous = V

                newRoot.sibling = nextSibling

                return newRoot

            # case "tau":
            #     E = root.first
            #     tempE = E
            #     newRoot = None
            #     aug = None
            #     tempESibling = None
            #
            #     gamma = Node("gamma")
            #     gammaL = Node("gamma")
            #
            #     gamma.sibling = gammaL
            #     gammaL.sibling = E
            #     tempESibling = E.sibling
            #     E.sibling = None
            #     aug = Node("aug")
            #     gammaL.first = aug
            #
            #     while E != None:
            #         gamma = Node("gamma")
            #         gammaL = Node("gamma")
            #         aug.sibling = gamma
            #         gamma.first = gammaL
            #         gammaL.sibling = E
            #         tempESibling = E.sibling
            #         E.sibling = None
            #         aug = Node("aug")
            #         gammaL.first = aug
            #         E = tempESibling
            #
            #     aug.sibling = Node('nil')
            #     tempE.sibling = None
            #     newRoot.sibling = nextSibling
            #
            #     return newRoot

            case Token.TokenType.WITHIN:
                if root.first.token.type == Token.TokenType.EQUALS and root.first.sibling.type == Token.TokenType.EQUALS :
                    eq1 = root.first
                    eq2 = eq1.sibling
                    X1 = eq1.first
                    E1 = X1.sibling
                    X2 = eq2.first
                    E2 = X2.sibling

                    newRoot = Node( Token.Token(Token.TokenType.EQUALS,"="))
                    newRoot.first = X2
                    gamma = Node( Token.Token(Token.TokenType.GAMMA,"gamma"))
                    lambdaNode = Node( Token.Token(Token.TokenType.LAMBDA,"lambda" ))

                    X2.sibling = gamma
                    gamma.previous = X2
                    gamma.first = lambdaNode
                    lambdaNode.sibling = E1
                    E1.previous = lambdaNode
                    lambdaNode.first = X1
                    X1.sibling = E2
                    E2.previous = X1
                    E1.sibling = None
                    newRoot.sibling = nextSibling

                    return newRoot
                else :
                    root.sibling = nextSibling

                    return root

            case Token.TokenType.AND:
                eq = root.first

                newRoot = Node( Token.Token(Token.TokenType.EQUALS,"="))
                comma = Node( Token.Token(Token.TokenType.COMMA,","))
                tau = Node( Token.Token(Token.TokenType.TAU,"tau"))

                newRoot.first = comma
                comma.sibling = tau
                tau.previous = comma

                X = eq.first
                E = X.sibling

                comma.first = X
                tau.first = E

                eq = eq.sibling
                while eq != None:
                    X.sibling = eq.first
                    eq.first.previous = X
                    E.sibling = eq.first.sibling
                    eq = eq.sibling
                    X = X.sibling
                    E = E.sibling

                X.sibling = None
                E.sibling = None
                newRoot.sibling = nextSibling


                return newRoot

            case Token.TokenType.REC:
                eq = root.first
                X = eq.first
                E = X.sibling

                new_root = Node( Token.Token(Token.TokenType.EQUALS,"="))
                new_root.first = X

                copy_X = X.createCopy()
                gamma = Node( Token.Token(Token.TokenType.GAMMA,"gamma"))
                X.sibling = gamma
                gamma.previous = X

                # TODO: may need to remove <> later !!!!
                y_star = Node( Token.Token(Token.TokenType.YSTAR,"Y*"))
                gamma.first = y_star
                lambda_ = Node( Token.Token(Token.TokenType.LAMBDA,"lambda"))
                y_star.sibling = lambda_
                lambda_.previous = y_star

                lambda_.first = copy_X
                copy_X.sibling = E
                E.previous = copy_X
                new_root.sibling = nextSibling


                return new_root

            case Token.TokenType.OP:
                E1 = root.first
                N = E1.sibling
                E2 = N.sibling

                new_root = Node( Token.Token(Token.TokenType.GAMMA,"gamma"))
                gamma_l = Node( Token.Token(Token.TokenType.GAMMA,"gamma"))

                new_root.first = gamma_l
                gamma_l.sibling = E2
                # E2.previous = gamma_l
                gamma_l.first = N
                N.sibling = E1
                # E1.previous = N
                E1.sibling = None
                new_root.sibling=nextSibling

                return new_root

            case _:
                return root

        # #print("root" , root.type)
        # root.previous = prevSibling
        # root.sibling = nextSibling
        return root

    # def createCopy(self, root):
    #     if root is None:
    #         return None
    #     node = Node(root.token)
    #     node.first = self.createCopy(root.first)
    #
    #     if root.sibling is not None:
    #         node.sibling = self.createCopy(root.sibling)
    #     return node


class TreeBuilder:
    def __init__(self):
        self.stack = []

    def get_tree(self):
        root = self.stack.pop()
        return root

    def create_copy(self, root):
        if root is None:
            return None
        node = Node(root.token)
        node.first = self.create_copy(root.first)

        if root.sibling is not None:
            node.sibling = self.create_copy(root.sibling)
        return node

    def preorder(self, root, level):
        if root is None:
            return
        dots = "." * level
        # print(root.token,"##############")
        if root.token.type == TokenType.ID:
            print_token_name = f"<ID:{root.token.name}>"
        elif root.token.type == TokenType.INTEGER:
            print_token_name = f"<INT:{root.token.name}>"
        elif root.token.type == TokenType.STRING:
            print_token_name = f"<STR:'{root.token.name}'>"
        elif root.token.type in [TokenType.NIL, TokenType.TRUE, TokenType.FALSE, TokenType.DUMMY, TokenType.YSTAR]:
            print_token_name = f"<{root.token.name}>"
        else:
            print_token_name = root.token.name

        print(dots + print_token_name + " ")
        self.preorder(root.first, level + 1)
        if root.sibling is not None:
            self.preorder(root.sibling, level)

    def print_tree(self):
        root = self.stack.pop()
        if root is None:
            print("!!!!!ERROR in PrintTree()!!!")
        self.preorder(root, 0)

    def build_tree(self, token, n):
        node = Node(token)
        if n == 0:
            self.stack.append(node)
        elif n == 1:
            stack_node = self.stack.pop()
            node.first = stack_node
            self.stack.append(node)
        elif n == 2:
            try:
                stack_node1 = self.stack.pop()
                stack_node2 = self.stack.pop()
                node.first = stack_node2
                stack_node2.sibling = stack_node1
                stack_node1.previous = stack_node2
                self.stack.append(node)
            except IndexError:
                import traceback
                traceback.print_exc()
        else:
            self.build_polyary_tree(n, node)

    def build_polyary_tree(self, n, new_node):
        temp = self.stack.pop()
        n -= 1
        while n > 0:
            right_node = self.stack.pop()
            right_node.sibling = temp
            temp.previous = right_node
            temp = right_node
            n -= 1
        new_node.first = temp
        self.stack.append(new_node)

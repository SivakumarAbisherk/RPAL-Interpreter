import token

import Token


class Node:


    def standarize(self, root):

        if root == None:
            return None


        root.first = self.standarize(root.first)

        if root.sibling != None:
            root.sibling = self.standarize(root.sibling)

        nextSibling = root.sibling

        # prevSibling = root.previous
        # nextSibling = root.sibling

        match root.type:
            case "let":
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

            case "where":
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

            case "function_form":
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

            case "within":
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

            case "and":
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

            case "rec":
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

            case "@":
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

    def __init__(self, type):
        self.type = type
        self.value = None
        self.sourceLineNumber = -1
        self.first = None
        self.sibling = None
        self.previous = None
        self.indentation = 0

    def print_tree(self):
        # #print(self.type)

        if self.first:
            # #print(" first of " + str(self.type) + " is ",end=" ")
            self.first.print_tree()
        if self.sibling:
            # #print(" sibling of " + str(self.type) + " is " ,end=" ")

            self.sibling.print_tree()

    def print_tree_to_cmd(self):

        for i in range(self.indentation):
            print(".", end="")
        if self.value is not None:
            print("<"+str(self.type.split(".")[1]) +":" + str(self.value)+">")
        else:print(str(self.type))
        # print(self.type, end=" ")
        # if self.first:
        #     #print("first of " + str(self.type) + " is ", self.first.type)
        # if self.sibling:
        #     #print("sibling of " + str(self.type) + " is ", self.sibling.type)
        #

        if self.first:
            self.first.indentation = self.indentation + 1
            self.first.print_tree_to_cmd()
        if self.sibling:
            self.sibling.indentation = self.indentation
            self.sibling.print_tree_to_cmd()

    # output to the file
    def print_tree_to_file(self, file):

        for i in range(self.indentation):
            file.write(".")
        # if(self.type ==)
        if self.value is not None:

            file.write("<"+str(self.type.split(".")[1])+":"+str(self.value)+">" + "\n")
        else :
            file.write(str(self.type) + "\n")

        if self.first:

            self.first.indentation = self.indentation + 1
            self.first.print_tree_to_file(file)
        if self.sibling:
            self.sibling.indentation = self.indentation
            self.sibling.print_tree_to_file(file)

    def createCopy (self):
        node = Node( self.type)
        node.value = self.value
        node.sourceLineNumber = self.sourceLineNumber
        node.first = self.first
        node.sibling = self.sibling
        node.previous = self.previous
        return node
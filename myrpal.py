import sys
# from CSEMachine import Evaluvator
from Parser import test_parser


def main():
    fn = ""
    is_print_ast = False
    is_print_st = False

    if len(sys.argv) == 1:
        fn = "t1.txt"
        is_print_ast = True
        is_print_st = True
    elif len(sys.argv) == 4 and ((sys.argv[1].lower() == "-ast" and sys.argv[2].lower() == "-st") or (sys.argv[1].lower() == "-st" and sys.argv[2].lower() == "-ast")):
        fn = sys.argv[3]
        is_print_ast = True
        is_print_st = True
    elif len(sys.argv) == 3:
        fn = sys.argv[2]
        if sys.argv[1].lower() == "-ast":
            is_print_ast = True
        elif sys.argv[1].lower() == "-st":
            is_print_st = True
        else:
            print("Invalid Arguments Passing!")
            return
    elif len(sys.argv) == 2:
        fn = sys.argv[1]
    else:
        print("Invalid Arguments Passing!")
        return
    test_parser(fn, is_print_ast, is_print_st)

    # result = Evaluvator.evaluate(fn, is_print_ast, is_print_st)
    # print(result)


if __name__ == "__main__":

    main()

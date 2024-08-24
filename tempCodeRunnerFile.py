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
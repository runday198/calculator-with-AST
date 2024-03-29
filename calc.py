all_symbols = ["+", "-", "*", "/", "(", ")"]
add_op = ["+", "-"]
mul_op = ["*", "/"]


def tokenize(exp: str):
    exp_list = [*exp]
    final_list = []
    digits = ""
    paren_count = 0

    for i in range(len(exp_list)):
        if exp_list[i].isdigit() or exp_list[i] == ".":
            digits += exp_list[i]
        elif exp_list[i] in all_symbols:
            if len(digits) > 0:
                final_list.append(digits)
            digits = ""
            final_list.append(exp_list[i])
            if exp_list[i] == "(":
                paren_count += 1
            elif exp_list[i] == ")":
                paren_count -= 1
                if paren_count < 0:
                    raise NameError("Invalid Input")
        else:
            raise NameError("Invalid symbol")

    if paren_count != 0:
        raise NameError("Invalid Input")

    if len(digits) > 0:
        final_list.append(digits)

    return final_list


class Node:
    def __init__(self, symbol, left, right):
        self.sym = symbol
        self.left = left
        self.right = right

    def syntax_tree(self):
        if len(self.sym) == 1:  # if length is one then this node is a leaf
            self.sym = self.sym[0]
        elif len(self.sym) == 0:  # if length is zero, then this node is empty
            self.sym = "0"  # this will only occur when we have a negative number, like this (-5)
        else:
            try:
                head, left, right = find_head(self.sym)
                # print(head, left, right)
            except NameError:
                # print("a")
                raise NameError("Invalid Input")

            self.sym = head
            self.left = Node(left, None, None)
            self.right = Node(right, None, None)

            try:
                self.left.syntax_tree()
                self.right.syntax_tree()
            except NameError:
                raise NameError("Invalid Input")

    def calculate(self):
        if self.sym not in all_symbols:
            return self.sym

        return eval(f"{self.left.calculate()} {self.sym} {self.right.calculate()}")

    def print(self):
        head = self
        if head.left != None:
            head.left.print()

        print(head.sym, end="")

        if head.right != None:
            head.right.print()


def find_head(token_list: list[str]):
    if len(token_list) == 0:
        # print("b")
        raise NameError("Invalid input")

    paren_count = 0
    mul_occured = False
    mul_index = 0

    # try to partition the expression on + | - operator if outside parentheses
    for i in range(len(token_list) - 1, -1, -1):
        token = token_list[i]
        if token == "(":
            paren_count += 1
        elif token == ")":
            paren_count -= 1
        elif token in add_op and paren_count == 0:
            return token, token_list[0:i], token_list[i + 1 :]
        elif token in mul_op and mul_occured is False and paren_count == 0:
            mul_occured = True
            mul_index = i

    # if this is reached then there is no + | - in the expression outside parentheses
    # so we can partition on * | /
    if mul_index != 0:
        return (
            token_list[mul_index],
            token_list[0:mul_index],
            token_list[mul_index + 1 :],
        )

    return find_head(token_list[1:-1])


def main():
    try:
        token_list = tokenize("(5+(6-2)*2)")
    except NameError:
        print("Invalid input")
        return

    head = Node(token_list, None, None)

    try:
        head.syntax_tree()
    except NameError:
        print("Invalid input")
        return

    print(head.calculate())


main()

from typing import List


class Node:
    def __init__(self, type, val, operands=[]):
        # self.id = id
        self.type = type
        # self.operator = operator
        self.operands = operands
        self.val = val

    def __repr__(self):
        return self.val


def preorder(root: Node, ans: list = None) -> List[str]:
    if not root:
        return ans
    if ans is None:
        ans = []
    ans.append(root.val)
    for child in root.operands:
        preorder(child, ans)
    return ans


def tree_2_infix(root: Node, stack=[]) -> List[str]:
    if not root:
        return stack

    if root.type == 'group':
        child_stack = []
        for child in root.operands:
            child_stack = tree_2_infix(child, child_stack)

        if len(child_stack) > 1:
            op = f" {root.val} "
            expression = f"( {op.join(child_stack)} )"
        else:
            expression = child_stack.pop()
        stack.append(expression)
    else:
        stack.append(root.val)

    return stack


def prefix_to_infix(prefix):
    stack = []

    # read prefix in reverse order
    i = len(prefix) - 1
    while i >= 0:
        if not is_operator(prefix[i]):
            # symbol is operand
            stack.append(prefix[i])
            i -= 1
        else:
            # symbol is operator
            if len(stack) > 1:
                expression = f"({stack.pop()} {prefix[i]} {stack.pop()})"
            else:
                expression = stack.pop()
            stack.append(expression)
            i -= 1

    return stack.pop()


def is_operator(c):
    return c in ['AND', 'OR']


if __name__ == '__main__':
    branch_1 = Node('group', 'OR', [Node('attribute', '1'), Node('attribute', '2'), Node('attribute', '3')])
    branch_2 = Node('group', 'OR', [Node('attribute', '4'), Node('attribute', '5')])
    branch_3 = Node('group', 'AND', [branch_2, Node('attribute', '6', [])])

    root = Node('group', 'AND', [branch_2])

    solution = preorder(root=root)
    infix = prefix_to_infix(solution)

    solution2 = tree_2_infix(root=root)

    print(solution)
    print(infix)
    print(solution2.pop())

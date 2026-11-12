import random


# ---------- Реалізація AVL-дерева ----------

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, level=0, prefix="Root: "):
        ret = "\t" * level + prefix + str(self.key) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


def get_height(node):
    return node.height if node else 0


def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0


def left_rotate(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def right_rotate(y):
    x = y.left
    T3 = x.right
    x.right = y
    y.left = T3
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def insert(root, key):
    if not root:
        return AVLNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root  # дублікати не додаємо

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1 and key < root.left.key:      # LL
        return right_rotate(root)
    if balance < -1 and key > root.right.key:    # RR
        return left_rotate(root)
    if balance > 1 and key > root.left.key:      # LR
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and key < root.right.key:    # RL
        root.right = right_rotate(root.right)
        return left_rotate(root)
    return root


# ---------- Сума всіх значень ----------

def tree_sum(root):
    """Рекурсивно: сума = значення вузла + сума лівого піддерева + сума правого.
    Час O(n) — кожен вузол відвідується один раз; пам'ять O(h) на стек рекурсії."""
    if root is None:
        return 0
    return root.key + tree_sum(root.left) + tree_sum(root.right)


def tree_sum_iterative(root):
    """Ітеративний варіант зі стеком (обхід у глибину)."""
    total = 0
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        total += node.key
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return total


# ---------- Перевірка ----------

root = None
keys = [10, 20, 30, 25, 28, 27, -1, 5, 15]
for key in keys:
    root = insert(root, key)

print("AVL-дерево:")
print(root)
print("Сума значень (рекурсивно):  ", tree_sum(root))
print("Сума значень (ітеративно):  ", tree_sum_iterative(root))
print("Перевірка через sum():      ", sum(keys))

# Автоматичні тести
assert tree_sum(None) == 0
assert tree_sum(insert(None, 42)) == 42

for _ in range(1000):
    data = random.sample(range(-10_000, 10_000), random.randint(1, 200))
    r = None
    for k in data:
        r = insert(r, k)
    assert tree_sum(r) == sum(data) == tree_sum_iterative(r)

print("Усі тести пройдено ✅")
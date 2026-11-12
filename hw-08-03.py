import heapq
import random
from itertools import combinations


def min_cost_connect_cables(cables):
    """Мінімальні витрати на з'єднання кабелів (жадібний алгоритм на мін-купі).
    Щоразу з'єднуємо два найкоротші кабелі, а результат повертаємо в купу.
    Повертає (загальні витрати, порядок з'єднань).
    Час O(n log n), пам'ять O(n)."""
    if len(cables) < 2:
        return 0, []

    heap = list(cables)
    heapq.heapify(heap)              # O(n)

    total_cost = 0
    order = []
    while len(heap) > 1:
        first = heapq.heappop(heap)  # найкоротший
        second = heapq.heappop(heap) # другий найкоротший
        cost = first + second
        total_cost += cost
        order.append((first, second, cost))
        heapq.heappush(heap, cost)   # новий кабель повертаємо в купу

    return total_cost, order


# ---------- Перевірка ----------

cables = [4, 3, 2, 6]
total, order = min_cost_connect_cables(cables)

print("Кабелі:", cables)
print("Порядок з'єднання:")
for step, (a, b, cost) in enumerate(order, 1):
    print(f"  Крок {step}: {a} + {b} = {cost}")
print("Загальні мінімальні витрати:", total)


# Перевірка повним перебором для малих наборів
def brute_force(cables):
    if len(cables) < 2:
        return 0
    best = float("inf")
    for i, j in combinations(range(len(cables)), 2):
        merged = cables[i] + cables[j]
        rest = [c for k, c in enumerate(cables) if k not in (i, j)] + [merged]
        best = min(best, merged + brute_force(rest))
    return best


assert min_cost_connect_cables([])[0] == 0
assert min_cost_connect_cables([5])[0] == 0
assert min_cost_connect_cables([1, 2])[0] == 3

for _ in range(300):
    data = [random.randint(1, 50) for _ in range(random.randint(1, 6))]
    assert min_cost_connect_cables(data)[0] == brute_force(data)

print("Усі тести пройдено ✅")
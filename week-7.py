
def bubble_up(heap, i):
    parrent = i // 2
    if i <= 1:
        return

    if heap[parrent] < heap[i]:
        heap[parrent], heap[i] = heap[i], heap[parrent]
        bubble_up(heap, parrent)

def bubble_down(heap, i):
    left_cild = i * 2
    right_cild = i * 2 + 1

    if left_cild >= len(heap):
        return

    max_cild = left_cild

    if right_cild < len(heap) and heap[right_cild] > heap[left_cild]:
        max_cild = right_cild

    if heap[i] < heap[max_cild]:
        heap[i], heap[max_cild] = heap[max_cild], heap[i]
        bubble_down(heap, max_cild)

def insert(heap, value):
    heap.append(value)
    bubble_up(heap, len(heap) - 1)


def extract_max(heap):
    if len(heap) <= 1:
        return None

    result = heap[1]
    last_element = heap.pop()

    if len(heap) == 1:
        return result

    heap[1] = last_element
    bubble_down(heap, 1)

    return result

heap = [0]


N = int(input())

for _ in range(N):
    inp = input().split()

    if inp[0] == 'N':
        insert(heap, (int(inp[2]), int(inp[1]))) # diff and then id
    else:
        result = extract_max(heap)
        print(result[1]) # id

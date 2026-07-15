def binary_search(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2

    if arr[mid] == target:                      # 1. 중간값이 찾으려는 값과 일치하는 경우
        return mid

    elif arr[mid] > target:                     # 2. 중간값이 타겟보다 큰 경우 -> 왼쪽 구간 탐색
        return binary_search(arr, target, low, mid - 1)

    else:                                       # 3. 중간값이 타겟보다 작은 경우 -> 오른쪽 구간 탐색
        return binary_search(arr, target, mid + 1, high)


data = [2, 5, 6, 8, 9, 11, 15, 18, 19, 22, 24, 25]
value = 15
result = binary_search(data, value, 0, len(data) - 1)

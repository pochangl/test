def bubble_sort(arr):
    """氣泡排序，逐步印出每一輪的比較與交換過程。"""
    n = len(arr)
    data = arr.copy()

    print(f"原始陣列: {data}\n")

    for i in range(n - 1):
        swapped = False
        print(f"=== 第 {i + 1} 輪 ===")

        for j in range(n - 1 - i):
            left, right = data[j], data[j + 1]
            marker = list("  " * n)
            marker[j] = "^"
            marker[j + 1] = "^"

            if left > right:
                data[j], data[j + 1] = right, left
                swapped = True
                print(f"  比較 {left} > {right} → 交換  {data}")
            else:
                print(f"  比較 {left} ≤ {right} → 不換  {data}")

        print(f"  第 {i + 1} 輪結果: {data}\n")

        if not swapped:
            print("未發生交換，排序提前完成！\n")
            break

    print(f"排序結果: {data}")
    return data


if __name__ == "__main__":
    sample = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort(sample)

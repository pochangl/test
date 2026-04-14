def bucket_sort(arr):
    if not arr:
        return arr

    min_val = min(arr)
    max_val = max(arr)

    if min_val == max_val:
        return list(arr)

    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]

    for num in arr:
        index = int((num - min_val) / (max_val - min_val) * (bucket_count - 1))
        buckets[index].append(num)

    for bucket in buckets:
        bucket.sort()

    return [num for bucket in buckets for num in bucket]


if __name__ == "__main__":
    data = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]
    print(f"排序前: {data}")
    print(f"排序後: {bucket_sort(data)}")

    data2 = [29, 25, 3, 49, 9, 37, 21, 43]
    print(f"排序前: {data2}")
    print(f"排序後: {bucket_sort(data2)}")

def merge_sort(parcels):
    """
    Sort parcels using Merge Sort.

    Sorting criteria:
    1. Lower priority number comes first.
    2. Earlier deadline comes first.
    """

    if len(parcels) <= 1:
        return parcels

    # Divide the list into two halves
    mid = len(parcels) // 2

    left = merge_sort(parcels[:mid])
    right = merge_sort(parcels[mid:])

    return merge(left, right)


def merge(left, right):
    """Combine two sorted lists into one sorted list."""

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        left_key = (left[i].priority, left[i].deadline)
        right_key = (right[j].priority, right[j].deadline)

        if left_key <= right_key:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result

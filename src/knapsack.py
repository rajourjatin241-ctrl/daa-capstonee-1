def knapsack(parcels, capacity):
    """
    Solve the 0/1 Knapsack problem using
    Dynamic Programming.

    Returns:
        selected_parcels: Optimal parcel selection
        dp: Complete DP table
    """

    n = len(parcels)

    # Create DP table
    dp = [
        [0 for _ in range(capacity + 1)]
        for _ in range(n + 1)
    ]

    # Fill DP table
    for i in range(1, n + 1):

        weight = parcels[i - 1].weight
        value = parcels[i - 1].value

        for w in range(capacity + 1):

            # Option 1: Do not select parcel
            dp[i][w] = dp[i - 1][w]

            # Option 2: Select parcel if it fits
            if weight <= w:

                include_value = (
                    value + dp[i - 1][w - weight]
                )

                dp[i][w] = max(
                    dp[i][w],
                    include_value
                )

    # Find selected parcels by backtracking
    selected_parcels = []

    remaining_capacity = capacity

    for i in range(n, 0, -1):

        if dp[i][remaining_capacity] != dp[i - 1][remaining_capacity]:

            parcel = parcels[i - 1]

            selected_parcels.append(parcel)

            remaining_capacity -= parcel.weight

    # Reverse to maintain original sorted order
    selected_parcels.reverse()

    return selected_parcels, dp

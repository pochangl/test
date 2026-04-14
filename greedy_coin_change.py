"""
Greedy Algorithm - Coin Change Problem (貪心演算法 - 找零錢問題)

Given a target amount and a set of coin denominations,
find the minimum number of coins needed using a greedy approach.

Greedy strategy: always pick the largest coin that doesn't exceed the remaining amount.
"""


def greedy_coin_change(amount, coins=(500, 100, 50, 10, 5, 1)):
    """
    Use greedy approach to make change for the given amount.

    Args:
        amount: target amount (integer)
        coins: available denominations, sorted descending

    Returns:
        list of (denomination, count) pairs
    """
    coins = sorted(coins, reverse=True)
    result = []
    remaining = amount

    for coin in coins:
        if remaining <= 0:
            break
        count = remaining // coin
        if count > 0:
            result.append((coin, count))
            remaining -= coin * count

    return result


def main():
    amount = 1367
    result = greedy_coin_change(amount)

    print(f"Amount: {amount}")
    print(f"Coins used:")
    total_coins = 0
    for coin, count in result:
        print(f"  {coin} x {count}")
        total_coins += count
    print(f"Total coins: {total_coins}")


if __name__ == "__main__":
    main()

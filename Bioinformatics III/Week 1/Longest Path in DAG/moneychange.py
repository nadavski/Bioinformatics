def min_number_of_coins(change:int, coins:list):
    '''
    :param change: Integer number representing money that should be returned as change.
    :param coins: Array of all possible coins nominal for a particular currency, in descending order. In this case [5, 4, 1].
    :return: Minimal number of coins for change.
    Creates list of minimum number of coins for each amount of money from 0 to change.
    '''
    minimum_number_of_coins = [0]*(change+1)
    for i in range(1, change+1):
        residuals_from_extracting_one_coin = [i-coin for coin in coins if i-coin >= 0]
        for j in residuals_from_extracting_one_coin:
            if minimum_number_of_coins[i] == 0 or minimum_number_of_coins[i] > minimum_number_of_coins[j]+1:
                minimum_number_of_coins[i] = minimum_number_of_coins[j]+1
    return minimum_number_of_coins[change]


if __name__ == '__main__':
    change = 24
    print(min_number_of_coins(change, [21, 7, 5, 3, 1]))  # 901

def exact_change_recursive(amount,coins):
    """ Return the number of different ways a change of 'amount' can be
        given using denominations given in the list of 'coins'
        >>> exact_change_recursive(10,[50,20,10,5,2,1])
        11
        >>> exact_change_recursive(100,[100,50,20,10,5,2,1])
        4563
    """
    assert amount >= 0
    
    if amount==0:
        # no amount left -> 1 solution exists with no coins
        return 1
    elif not coins:
        # amount>0, no coins left -> no solution possibe
        return 0
    else:
        current_denomination = coins[0]
        remaining_coins = coins[1:]
        running_total = 0
        solutions_count = 0
        # Create solutions with increasing numbers of coins of the current_denomination
        while running_total<= amount:
            # reaming_amount needs to be achieved with remaining_coins
            remaining_amount = amount - running_total
            solutions_count += exact_change_recursive(remaining_amount,remaining_coins)
            running_total += current_denomination
        return solutions_count

def exact_change_recursive_print(amount,coins,current_change=""):
    assert amount >= 0
    
    if amount==0:
        # no amount left -> 1 solution exists with no coins
        print(current_change[1:])
        return 1
    elif not coins:
        # amount>0, no coins left -> no solution possibe
        return 0
    else:
        current_denomination = coins[0]
        remaining_coins = coins[1:]
        running_total = 0
        current_denomination_count = 0
        solutions_count = 0
        while running_total<= amount:
            remaining = amount - running_total
            new_change = current_change + ",{}x{}ct".format(current_denomination_count,current_denomination)
            solutions_count += exact_change_recursive_print(remaining,remaining_coins,new_change)
            current_denomination_count += 1
            running_total = current_denomination_count * current_denomination
        return solutions_count

def exact_change_dynamic(amount,coins):
    """
    counts[x] counts the number of ways an amount of x can be made in exact change out of a subset of coins
    given in the list of denominations 'coins'.
    Initially there are no possibilities, if no coins are allowed
    >>> exact_change_dynamic(20,[50,20,10,5,2,1])
    [1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 19, 22, 25, 28, 31, 34, 41]
    >>> exact_change_dynamic(100,[100,50,20,10,5,2,1])[-10:]
    [3229, 3376, 3484, 3631, 3778, 3925, 4072, 4219, 4366, 4563]
    """
    counts = [0]*(amount+1)
    # Except: there is 1 way to get a change of 0 ct using no coins
    counts[0] = 1
    # Recalculate counts by allowing additional denominations from coins one by one
    for denomination in coins:
        for x in range(denomination,amount+1):
            # Using an additional coin of 'denomination' we have an additional 'counts[x-denomination]' possibilities
            #
            counts[x] += counts[x-denomination]
    return counts
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
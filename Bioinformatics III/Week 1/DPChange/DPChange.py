def interpreter(conn):
    nn = int(conn.readline().strip())
    dd = map(int,conn.readline().strip().split(','))
    return nn, dd

def DPchange(money,coins):
	minNumCoins = [0] * (money+1)
	for m in range(1,money+1):
		minNumCoins[m] = float("inf")
		for coin in coins:
			if m >= coin:
				if minNumCoins[m-coin] + 1 < minNumCoins[m]:
					minNumCoins[m] = minNumCoins[m-coin] + 1
	return minNumCoins[-1]

if __name__ == '__main__':
	money = 19893
	coins = [24,11,8,5,3,1]
	minNum = DPchange(money,coins)
	print (minNum)
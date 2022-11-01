def main_alg(n, m, sh, thick):
    shoes = sh.copy()
    m += 1
    del1 = m
    res = []
    for i in range(n):
        shoes[i] += thick

    for p in range(n):
        a = [False] * m
        colored = [[False for _ in range(n)] for _ in range(m)]

        colored[sh[p]][p] = True

        a[sh[p]] = True

        for i in range(p, m):
            for j in range(n):
                if (i - shoes[j] >= 0) and (not colored[i - shoes[j]][j]) and (a[i - shoes[j]]):
                    a[i] = True
                    colored[i][j] = True
                    for k in range(j):
                        colored[i][k] = colored[i - shoes[j]][k]

                    for k in range(j + 1, n):
                        colored[i][k] = colored[i - shoes[j]][k]
                    break

        for i in range(m - 1, -1, -1):
            if a[i] and del1 > m - i - 1:
                del1 = m - i - 1

                k = 0
                for j in range(n):
                    if colored[i][j]:
                        k += 1

                k += 1
                res = [0] * k
                res[0] = del1
                k = 1

                for j in range(n):
                    if colored[i][j]:
                        res[k] = sh[j]
                        k += 1
                break
    return res

class TubeUnion:
    def __init__(self, arg):
        self.tubes = [arg] if type(arg) is int else arg
        self.total_len = sum(self.tubes)

    def __add__(self, other):
        tmp = self.tubes.copy()
        tmp.extend(other.tubes)
        return TubeUnion(tmp)

    def __str__(self):
        return f"{self.tubes}"

    def __le__(self, other):
        return self.total_len <= other.total_len

    def __ge__(self, other):
        return self.total_len >= other.total_len

    def __lt__(self, other):
        return self.total_len < other.total_len

    def __repr__(self):
        return self.tubes


def optimal_cutting(capacity, weight, cutter_len):
    capacity += cutter_len
    n = len(weight)
    dp = [[TubeUnion(0) for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                dp[i][w] = TubeUnion(0)
            elif weight[i - 1] + cutter_len <= w:
                dp[i][w] = max(TubeUnion(weight[i - 1] + cutter_len) + dp[i - 1][w - weight[i - 1] - cutter_len], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]




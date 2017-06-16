def suffixArray(s):
    n = len(s)
    rkd = {c: i for i, c in enumerate(sorted(set(s)))}
    rank = [rkd[c] for c in s]
    k = 1
    while k <= n:
        xy = [(rank[i], (rank[i+k] if i+k < n else -1)) for i in xrange(n)]
        rkd = {c: i for i, c in enumerate(sorted(set(xy)))}
        rank = [rkd[c] for c in xy]
        k *= 2
    sa = [0] * n
    for i in xrange(n):
        sa[rank[i]] = i

    height = [0] * n
    h = 0
    for i in xrange(n):
        if rank[i]:
            if h > 0:
                h -= 1
            j = sa[rank[i]-1]
            while i+h < n and j+h < n and s[i+h] == s[j+h]:
                h += 1
        else:
            h = 0
        height[rank[i]] = h

    return sa, height

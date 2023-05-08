import math

def update(g, marks, a):
    for m in marks:
        if m[1] != '-':
            znak = g[m[2]][m[1]][2] # 1/-1 как множитель

            # остаточные пропускные способности ребер, составляющих сквозной путь,
            # уменьшаются на величину а в направлении движения потока
            g[m[2]][m[1]][0] -= znak * a
            # и увеличиваются на эту же величину в противоположном направлении
            g[m[2]][m[1]][1] += znak * a
            # обновляем веса ребер как и (j,i), так и (i,j), потому что матрица симметрична
            g[m[1]][m[2]][0] -= znak * a
            g[m[1]][m[2]][1] += znak * a

g = [[[0,0,1], [20,0,1], [30,0,1], [10,0,1], [0,0,1]],
     [[20,0,-1], [0,0,1], [40,0,1], [0,0,1], [30,0,1]],
     [[30,0,-1], [40,0,-1], [0,0,1], [10,0,1], [20,0,1]],
     [[10,0,-1], [0,0,1], [10,0,-1], [0,0,1], [20,0,1]],
     [[0,0,1], [30,0,-1], [20,0,-1], [20,0,-1], [0,0,1]],
]
g = [[[0,0,1], [4,0,1], [3,0,1], [0,0,1], [0,0,1]],
     [[4,0,-1], [0,0,1], [1,0,1], [0,0,1], [3,0,1]],
     [[3,0,-1], [1,0,-1], [0,0,1], [6,0,1], [1,0,1]],
     [[0,0,-1], [0,0,1], [6,0,-1], [0,0,1], [2,0,1]],
     [[0,0,1], [3,0,-1], [1,0,-1], [2,0,-1], [0,0,1]],
]
n = len(g)
start = 0 # вершина истока
end = 4 # вершина стока
mark_start = (math.inf, '-', start)
f = [] # максимальные потоки найденных маршрутов

# алгоритм заканчивается, когда множество S узлов, в которые можно перейти из истока - пустое
# 1 -> 2 -> 4 -> 6 (шаги)
k = start
while k != '-':
    # шаг 1. Полагаем начальную вершину как исток
    i = start
    # шаг 2-3.
    marks = [mark_start] # (вес, куда, откуда)
    use_v = {i}
    while i != end: # пока не дойдем до стока
        max_znach = 0
        k = '-' # выбираем вершину, где ребро (i,k) имеет макс. пропускную способность
        for j in range(len(g[i])):
            if j in use_v: # узел j должен быть не помеченным
                continue
            if g[i][j][2] == 1: # движение в прямом напралении
                if g[i][j][0] > max_znach: # остаточная пропускная способностьдолжна быть положительна
                    max_znach = g[i][j][0]
                    k = j
            else: # движение в обратном направлении
                if g[i][j][1] > max_znach:
                    max_znach = g[i][j][1]
                    k = j
        # шаг 4. (откат назад)
        if k == '-': # S - пустое
            if i == start:
                # сквозной путь невозможен
                # алгоритм заканчивается ... шаг 6.
                break
            else:
                # перейти на предыдущий узел по метке и удалить его из S
                i = marks.pop()[2]
                continue
        use_v.add(k) # добавляем выбранную вершину во множество использованных
        if g[i][k][2] == 1: # определяем вес ребра (i,k)
            m = g[i][k][0]
        else:
            m = g[i][k][1]
        marks.append((m, k, i)) # добавляем метку маршрута (запоминание предыдущей вершины необходимо для шага 4 (отката назад),
        # а помнить текущую пригодится для того, чтобы в шаге 5 определить остаточные пропускные способности ребер)
        if k == end: # если дошли до стока (к-ая вершина - сток)
            # шаг 5. находим максимальную пропускную способность маршрута
            f.append(min([a[0] for a in marks]))
            # обновляем остаточные пропускные способности ребер
            update(g, marks, f[-1])
            break
        i = k
# шаг 6. Вычисляем максимальный поток как сумму найденных сквозных путей
print(f'Максимальный поток в сети: {sum(f)}')
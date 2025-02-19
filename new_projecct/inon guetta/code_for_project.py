b = {
    'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן','o':'ם', 'p': 'פ',
    'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל',
    'l': 'ך',';':'ף',
    'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ',',':'ת'
    ,'.':'ץ'
}

keys = list(b.keys())
values = list(b.values())
c = {}
for i in range(len(keys)):
    c[values[i]] = keys[i]



arr = [
    'a', 'a', 'a', 'b', 'b', 'b', 'a', 'g', 'g', 'g', 'g',
    'd', 'alt', 'shift', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h',
    'h', 'j', 'j', 'j', 'j', 'o', 'o', 'o', 'o', 'o','a', 'a', 'a', 'b', 'b', 'b', 'a', 'g', 'g', 'g', 'g',
    'd',
]
def to_change(arr, b):
    x = False
    one = 'flag1'
    arr2 = []
    i = 0
    while i < len(arr):

        if i < len(arr) - 1:

            if arr[i] == 'alt' and arr[i + 1] == 'shift':
                x = True
                arr2.append(one)
                i += 2
                continue

        if x and arr[i] in b:
            arr2.append(b[arr[i]])
        else:
            arr2.append(arr[i])
        i += 1

    arr3 = []
    x = 0
    for i in range(len(arr2)):
        if arr2[i] == one:
            x = i
    for j in range(x+1,len(arr2)):
        arr3.append(arr2[j])

    arr3 = arr3[::-1]
    a = []
    y = True
    for i in range(len(arr2)):
        if arr2[i] == one:
            y = False
        if y:
            a.append(arr2[i])

    arr4 = arr3 + a
    return arr4


a = to_change(arr, b)
print(a)



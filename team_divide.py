import random

dosiler_listi = [
    "Babirov",
    "Faiq",
    "Rewid",
    "Maga",
    "Yashar",
    "Emil",
    "Farhad",
    "Reyego",
    "Hikmet",
    "Farid",
    "Elwan",
    "Kenan",
]


def divide_to_2_teams(list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]


print(divide_to_2_teams(dosiler_listi, 2))

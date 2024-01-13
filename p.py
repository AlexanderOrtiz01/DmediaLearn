import random

sample_list = ['A', 'B', 'C', 'D', 'E']
print("Lista original:")
print(sample_list)

random.shuffle(sample_list)
print("\nDespués de la primera mezcla:")
print(sample_list)

random.shuffle(sample_list)
print("\nDespués de la segunda mezcla:")
print(sample_list)

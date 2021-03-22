# Just an example app.
# It will get two lists and print the min of each list.
# @See ./examples/example_app.py for explanation.

list1 = [int(x) for x in input().split()]
list2 = [float(x) for x in input().split()]
print(min(list1))
print(min(list2))

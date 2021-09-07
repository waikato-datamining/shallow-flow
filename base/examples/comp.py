from shallowflow.api.compatibility import is_compatible, Unknown


def check(output, input):
    print("\noutput:", output, "->", "input:", input)
    print(is_compatible(output, input))


output = object
input = object
check(output, input)

output = [float]
input = [int, float]
check(output, input)

output = [float]
input = str
check(output, input)

output = [float]
input = Unknown
check(output, input)

output = list
input = list
check(output, input)

output = list
input = str
check(output, input)

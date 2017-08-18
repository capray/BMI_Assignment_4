# taking mark's advice this list comprehension inverts the contents of each element (i.e. cell) in the array
column1_array = [cell[::-1] for cell in column1_array]

rex = re.compile(r'(?:(?P<Dilution> *[0]+1) *)?(?:(?P<Visit> *[1-3][v|V] *))?(?P<PatientID>[ |[A-Za-z0-9_]+)')
outputs = [rex.match(x) for x in column1_array]

# this takes the named groups from the regular expression above converts everything into a list of dictionaries where
# the keys are group names (PatientID, Visit and Dilution) and the values are the corresponding string components
lst_of_dcts = []
for i, o in enumerate(outputs):
    try:
        lst_of_dcts.append(o.groupdict())
        # print(o.groupdict())
    except:
        print(column1_array[i])
# print(lst_of_dcts)

rex = re.compile # basically re.complile() is a more computationally efficent
# way of writing a regular expression. It turns the regular expression into
# an 'Regex object' which can be referred to by other methods like .match().
# The computer can just use the compiled regex object instead of 'looking  up'
# the regular expression each it time it may appear in the program.
# Also, it just makes the code look better since it breaks things up into
# two lines and not just one super long line.
# It would have been equivilant if I wrote the following:

# outputs = []
# for element in column1_array:
#     outputs.append(re.match(r'(?:(?P<Dilution> *[0]+1) *)?(?:(?P<Visit> *[1-3][v|V] *))?(?P<PatientID>[ |[A-Za-z0-9_]+)', element))


(?:(?P<Dilution> *[0]+1) *)? # The outer set of brackets with the ?: is
# a non-capturing group. The inner set of brackets starting with the ?P<> is the
# 'named caputuring group' called 'Dilution.' The ' *' means zero or more spaces.
# The [0]+1 means one or more zeros followed by a 1. The ? means that the
# whole previous expression is optional and may not appear.

# The ?P<> named capturing group allows a portion of the substring to be
# labled and makes it accessible by that label

# The ?:() is non capturing meaning, the enclosed part is ignored, but is still
# required for the whole expression to match. Its nessecary because
# the space* following the Dilution group was acting 'greedy' and kept on grabbing
# the visit in certain cases where the cell formatting was espeically bad.
# Since the space is outside the optional named capturing group but inside
# the non-capturing group the space is required for the substring to match,
# but is ignored when the substring is returned, and thus prevents the space
# from being 'greedy.'

(?:(?P<Visit> *[1-3][v|V] *))? # The visit expression of the regular expression
# statement has the same format as the Dilution one. Only diference is
# that [1-3][v|V]  means any number in the set 1-3 followed by a lowercase
# 'v' or upper case 'V.'

(?P<PatientID>[ |[A-Za-z0-9_]+) # Unlike the earlier ones, the PatientID
# expression does not have a ? which would make it optional. This is because
# an ID appears in every cell in the excel file.
# The [ |[A-Za-z0-9_]+ means a space or any upper/lower case letter,
# digit or underscore one or more times.

rex.match(x) # If zero or more characters at the beginning of string match the
# regular expression pattern, return a corresponding MatchObject
# (i.e boolean value of True) instance.
# Return None if the string does not match the pattern.

o.groupdict() # Return a dictionary containing all the named subgroups of the
# match, keyed by the subgroup name. The default argument is used for groups
# that did not participate in the match; it defaults to None

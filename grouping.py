import random
def div_students_by_2(students):
    # calculate how many groups
    group_number, rem = divmod(len(students), 2)
    gcs = [2 for i in range(group_number)]
    if rem == 1:
        gcs[-1] += 1
    groups = _populate_groups(students, gcs)
    return tuple(groups)

def _populate_groups(students, gcs):
    groups = [list() for i in range(len(gcs))] 
    for i, g in enumerate(groups):
        for j in range(gcs[i]):
            s_candidate = random.choice(students)
            students.remove(s_candidate)
            g.append(s_candidate)
    return groups

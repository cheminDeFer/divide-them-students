import random
import warnings
def div_students_by_n(students, n : int):
    assert n > 1, "n should be greater than 1"
    # calculate how many groups
    group_number, rem = divmod(len(students), n)
    gcs = [n for i in range(group_number)]
    for i in range(rem):
        gcs[-i] += 1

    groups = _populate_groups(students, gcs)
    return tuple(groups)

def div_students_by_2(students):
    warnings.warn(
        "div_students_by_2 is deprecated please "
        "use div_students_by_n instead.",
        DeprecationWarning,
        stacklevel=2
        )
    return div_students_by_n(students, 2)

def _populate_groups(students, gcs):
    groups = [list() for i in range(len(gcs))] 
    for i, g in enumerate(groups):
        for j in range(gcs[i]):
            s_candidate = random.choice(students)
            students.remove(s_candidate)
            g.append(s_candidate)
    return groups


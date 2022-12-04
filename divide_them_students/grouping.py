import random


def div_students_by_n(students, n: int):
    assert n > 1, "n should be greater than 1"
    # calculate how many groups
    group_number, rem = divmod(len(students), n)
    gcs = [n for i in range(group_number)]
    if rem > len(gcs):
        gcs.append(rem)
    else:
        for i in range(rem):
            gcs[-i - 1] += 1

    return _populate_groups(students, gcs)


def _populate_groups(students, gcs):
    groups = [list() for i in range(len(gcs))]
    for i, g in enumerate(groups):
        for j in range(gcs[i]):
            s_candidate = random.choice(students)
            students.remove(s_candidate)
            g.append(s_candidate)
    return tuple([tuple(i) for i in groups])


def dump_grouping(grouping):
    result = ""
    for group in grouping:
        for student in group:
            result += str(student) + ", "
        result += "\n"

    return result[:-1]

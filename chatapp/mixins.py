from chatapp.models import Thread


# For always correct thread DB participant1/participant2 sequence
def correct_sequence(serializer):
    id1 = int(str(serializer.data['participant1']))
    id2 = int(str(serializer.data['participant2']))

    if id1 > id2:
        return id2, id1
    return id1, id2


def correct_users(serializer):
    return str(serializer.data['participant1']) != str(serializer.data['participant2'])


def thread_exists(serializer):
    obj = False

    id1, id2 = correct_sequence(serializer)
    if Thread.objects.filter(participant1=id1, participant2=id2):
        obj = Thread.objects.get(participant1=id1, participant2=id2)
    return obj


def correct_user_ids(parts, user_ids):
    for part in parts:
        if part not in user_ids:
            return False
    return True

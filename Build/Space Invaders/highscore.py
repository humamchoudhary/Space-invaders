

def Get_High(cur_score):
    file = open('data.txt', 'r')

    for each in file:
        if cur_score > int(each):
            write_high(str(cur_score))
        return each
    file.close()


def write_high(highscore):
    file = open('data.txt', 'w')
    file.write(highscore)
    file.close()

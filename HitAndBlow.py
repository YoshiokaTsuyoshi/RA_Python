count = 0
hit = 0
blow = 0
ans = [1, 2, 3]

#予想プログラムで使用する変数
choices = [i for i in range(10)]
history = [[] for _i in range(4)]
zero_flag = False
flag = 0

print("重複しない0～9の数字で三桁の数を思い浮かべてください。")
print("こちらの予想した数に対してHitとBlowの数を入力してください。")

while True:
    count += 1
    print("思い浮かべた数は「{} {} {}」ですか？".format(ans[0], ans[1], ans[2]))
    hit = int(input("Hit -> "))
    blow = int(input("Blow -> "))
    
    if hit == 3:
        break
    if hit + blow == 0:
        choices.remove(ans[0])
        choices.remove(ans[1])
        choices.remove(ans[2])
    if hit + blow == 3 and flag < 20:
        flag = 10
        if hit == 1:
            flag = 20


    #予想プログラムで使う用の履歴を格納
    history[0].append(ans[0] * 100 + ans[1] * 10 + ans[2])
    history[1].append(hit)
    history[2].append(blow)
    history[3].append(hit + blow)


    #以下予想プログラム(最短ではない)
    if flag == 0:
        ans = [4, 5, 6]
        flag += 1
    elif flag == 1:
        ans = [7, 8, 9]
        flag += 1
        temp_sum = 0
        for i in history[3]:
            temp_sum += i
        if temp_sum == 3:
            flag += 1
            choices.remove(ans[0])
            choices.remove(ans[1])
            choices.remove(ans[2])
    elif flag == 2:
        temp_sum = 0
        for i in history[3]:
            temp_sum += i
        zero_flag = temp_sum != 3
        flag += 1
    if flag == 3:
        if zero_flag:
            if len(choices) == 7:
                ans = [choices[1], choices[4], choices[0]]
            else:
                ans = [choices[0], choices[1], choices[2]]
        else:
            choices.remove(0)
            ans = [choices[0], choices[1], choices[3]]
        flag += 1
    elif flag == 4:
        if zero_flag:
            if len(choices) == 7:
                ans = [choices[2], choices[5], choices[0]]
            else:
                ans = [choices[0], choices[2], choices[3]]
        else:
            if len(choices) == 3:
                ans = choices
            elif history[3][-1] == 0 and len(choices) == 6:
                ans = [choices[1], choices[3], choices[4]]
            else:
                ans = [choices[1], choices[2], choices[3]]
        flag += 1
    elif flag == 5:
        if zero_flag:
            if len(choices) == 7:
                ans = [choices[3], choices[6], choices[0]]
            else:
                ans = [choices[0], choices[3], choices[1]]
        else:
            if len(choices) == 3:
                ans = choices
            elif history[3][-1] == 0 and len(choices) == 6:
                ans = [choices[1], choices[3], choices[4]]
            elif history[3][-2] == 0 and len(choices) == 6:
                ans = [choices[1], choices[4], choices[5]]
            elif len(choices) == 9:
                if history[3][-2] - history[3][-1] > 0:
                    choices.pop(5)
                    choices.pop(4)
                    choices.pop(2)
                    choices.pop(1)
                    ans = [choices[0], choices[1], choices[2]]
                elif history[3][-2] - history[3][-1] < 0:
                    choices.pop(5)
                    choices.pop(4)
                    choices.pop(1)
                    choices.pop(0)
                    ans = [choices[0], choices[1], choices[2]]
                else:
                    if max(history[3][-2], history[3][-1]) == 2:
                        choices.pop(5)
                        choices.pop(4)
                        choices.pop(2)
                        choices.pop(0)
                        ans = [choices[0], choices[1], choices[2]]
                    else:
                        choices.pop(3)
                        choices.pop(2)
                        choices.pop(0)
                        ans = [choices[1], choices[3], choices[4]]
            else:
                temp_bool = True
                for i in range(3):
                    if history[3][i] == 1:
                        temp_bool = True
                    if history[3][i] == 2:
                        temp_bool = False
                if history[3][-2] - history[3][-1] > 0:
                    if temp_bool:
                        choices.pop(3)
                        choices.pop(2)
                    else:
                        choices.pop(2)
                        choices.pop(1)
                elif history[3][-2] - history[3][-1] < 0:
                    if temp_bool:
                        choices.pop(3)
                        choices.pop(0)
                    else:
                        choices.pop(1)
                        choices.pop(0)
                else:
                    if history[3][-1] == 2:
                        choices.pop(2)
                        choices.pop(0)
                    else:
                        choices.pop(3)
                        choices.pop(2)
                        choices.pop(0)
                ans = [choices[0], choices[1], choices[2]]
        flag += 1
    elif flag == 6:
        if zero_flag:
            if len(choices) == 7:
                temp_list = []
                for i in range(len(history[0]) - 3, len(history[0])):
                    if history[3][i] == 2:
                        temp_list.append(history[0][i])
                ans = [int(temp_list[0] / 100) % 10, int(temp_list[1] % 100 / 10), 0]
            else:
                ans = [0, 0, 0]
                break
        else:
            if len(choices) == 3:
                ans = choices
            elif len(choices) == 6:
                ans = [choices[1], choices[4], choices[5]]
            elif len(choices) == 5:
                ans = [choices[0], choices[1], choices[3]]
            elif len(choices) == 4:
                ans = [choices[0], choices[1], choices[3]]
        flag += 1
    elif flag == 7:
        if zero_flag:
            if len(choices) == 7:
                temp_list = []
                for i in range(len(history[0]) - 4, len(history[0]) - 1):
                    if history[3][i] == 2:
                        temp_list.append(history[0][i])
                ans = [int(temp_list[0] % 100 / 10), int(temp_list[1] / 100) % 10, 0]
            else:
                ans = [0, 0, 0]
                break
        else:
            if len(choices) == 3:
                ans = choices
            elif len(choices) == 6:
                if history[3][-2] - history[3][-1] > 0:
                    ans = [choices[0], choices[1], choices[3]]
                elif history[3][-2] - history[3][-1] < 0:
                    ans = [choices[0], choices[1], choices[5]]
                else:
                    if max(history[3][-2], history[3][-1]) == 2:
                        ans = [choices[0], choices[1], choices[4]]
                    else:
                        ans = [choices[0], choices[2], choices[4]]
            elif len(choices) == 5:
                ans = [choices[0], choices[1], choices[4]]
            elif len(choices) == 4:
                ans = [0, 0, 0]
                break
        flag += 1
    elif flag == 10:
        temp = ans[0]
        ans[0] = ans[1]
        ans[1] = ans[2]
        ans[2] = temp
    elif flag == 20:
        temp = ans[1]
        ans[1] = ans[2]
        ans[2] = temp
        flag += 1
    elif flag == 21:
        temp = ans[0]
        ans[0] = ans[1]
        ans[1] = ans[2]
        ans[2] = temp
        flag += 1
    elif flag == 22:
        temp = ans[0]
        ans[0] = ans[1]
        ans[1] = ans[2]
        ans[2] = temp
        flag += 1

if ans == [0, 0, 0]:
    print("予想不可能：回答を間違えていませんか？")
else:
    print("予想回数：{}回　あなたの思い浮かべた数「{} {} {}」".format(count, ans[0], ans[1], ans[2]))
A = 90-100
B=80-89
C=60-79
D=40-59
E=0-39

score = int(input("输入分数:"))

if score > 100:
    print("我擦，最高分才100...")
elif score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >=70:
    print("E")

else:
    print("太笨了...E")
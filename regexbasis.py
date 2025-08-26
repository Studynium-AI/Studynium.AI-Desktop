# import re


def reg(prompt:str):
    search = answer = 0
    lst = prompt.split("\n")
    for i in range(len(lst)):
        if ("search" in lst[i].lower())and(":" in lst[i]):
            search = i
        elif (("answer" in lst[i].lower())or("response" in lst[i].lower()))and(":" in lst[i]):
            answer = i
    search,answer = "\n".join(lst[search:answer+1]),"\n".join(lst[search:])
    return search,answer

if __name__ == "__main__":
    x = """answer
    hello world
    """
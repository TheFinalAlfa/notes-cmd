import readline


def dynamic_input(prompt, *prefill: list, max_rows=0) -> str:
    ## Args form: (prompt, prefill)
    result = []
    i = 0
    print(prompt, end="")
    try:
        while True:
            if i < len(prefill):
                readline.set_startup_hook(lambda: readline.insert_text(prefill[i]))
            else:
                readline.set_startup_hook()
            result.append(input())
            if result[-1] == "" :
                return "\n".join(result[:-1])
            if (i + 1 == max_rows and max_rows != 0):
                return "\n".join(result)
            else:
                i += 1
    finally:
        readline.set_startup_hook()
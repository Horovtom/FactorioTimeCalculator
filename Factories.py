craft_amount = None
craft_time = None
result_amount = None
speed_modifiers = {}
machines = {}
factories = 0


def gen_pos(generated: list, m, depth, n):
    if depth == n:
        if sum(generated) == m:
            return [generated.copy()]
    else:
        result = []
        suma = sum(generated)
        for i in range(m - suma + 1):
            r = generated.copy()
            r.append(i)
            possibilities = gen_pos(r, m, depth + 1, n)
            if possibilities is None:
                continue
            for k in possibilities:
                result.append(k)
        return result


def generate_speed_modifiers(possible_modules):
    for machine_name in machines:
        res = []

        for possibility in gen_pos([], machines[machine_name]["module_slots"], 0, len(possible_modules)):
            increment = 0
            for module in range(len(possible_modules)):
                increment += possible_modules[module] * possibility[module]

            res.append(increment)

        # Make values unique and sorted from the highest to the lowest
        res = list(set(res))
        res.sort()
        res.reverse()
        speed_modifiers[machine_name] = res


def resulting_amount(machine_speed, machines, modules) -> float:
    return (craft_amount / craft_time) * machines * machine_speed * (1 + (modules / 100))


def deep_copy(speed_modifiers):
    res = {}
    keys = list(speed_modifiers.keys())
    for key in keys:
        res[key] = speed_modifiers[key].copy()
    return res


def step(amount_so_far, target_amount, how, machine_names, speeds):
    usable_machine_names = machine_names.copy()
    usable_speeds = deep_copy(speeds)
    for machine_name in machine_names:
        for speed in speeds[machine_name]:
            generated_amount = resulting_amount(machines[machine_name]["craft_speed"], 1, speed) + amount_so_far
            new_how = str(how) + " " + str(machine_name) + ":" + str(speed)
            if generated_amount == target_amount:
                res = get_result(new_how)
                if factories == 0 or res[1] == factories:
                    print(res[0])
                # resut(get_result(new_how))
            elif generated_amount > target_amount:
                break
            else:
                step(generated_amount, target_amount, new_how, usable_machine_names,
                     usable_speeds)
            usable_speeds[machine_name].remove(speed)

        usable_machine_names.remove(machine_name)


def get_result(line):
    tokens = line.split(" ")
    tokens_unique = set(tokens)
    res = ""
    factory_count = 0
    for token in tokens_unique:
        if token != "":
            count = tokens.count(token)
            res += "{:>2}x{:<5} ".format(str(count), token)
            factory_count += count
    return [str(factory_count) + " - " + res, factory_count]


if __name__ == "__main__":
    craft_amount = int(input("What is the craft amount? (How many items per craft cycle) "))
    craft_time = float(input("What is the craft time? (How long does the craft cycle take) "))
    result_amount = float(input("How many items do you want to craft? "))
    factories = int(input("How many factories do you want to use? (0 for undefined)"))

    machines = {
        "Y": {"craft_speed": 1.25, "module_slots": 4},
        "B": {"craft_speed": 0.75, "module_slots": 2},
        "G": {"craft_speed": 0.5, "module_slots": 0}}
    machine_types = [
        "Y",
        "B",
        "G"
    ]

    generate_speed_modifiers([0, 20, 30, 50])

    step(0, result_amount, "", machine_types, deep_copy(speed_modifiers))

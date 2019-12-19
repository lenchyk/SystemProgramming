# Lab 2

right_signals = ["dlm", "cfr", "ltr"]
example_signals = ["dlm", "dkk", "dlm", "cfr", "ltr", "cfr", "ltr"]
signals = input("Enter signals, please: \n").lower().split()

unchangeable_signals = [0, 1, 2, 4, 6, 7, 8]


def move(current_state, signal):
    if current_state in unchangeable_signals and signal in right_signals:
        print("S{0} --> S{1} ({2})".format(current_state, current_state + 1, signal))
        current_state += 1
    elif current_state == 3:
        if signal == "ltr":
            print("S{0} --> S{0} ({1}, didn't changed)".format(current_state, signal))
            current_state += 0
        elif signal == "cfr":
            print("S{0} --> S{1} ({2})".format(current_state, current_state + 1, signal))
            current_state += 1
        elif signal == "dlm":
            current_state = 7
            print("S{0} --> S{1}".format(3, current_state))
        else:
            print("Signal is incorrect for S3!")
    elif current_state == 5:
        if signal == "dlm" or signal == "ltr":
            print("S{0} --> S{1} ({2})".format(current_state, current_state + 1, signal))
            current_state += 1
        elif signal == "cfr":
            current_state = 8
            print("S{0} --> S{1}".format(5, current_state))
        else:
            print("S{0} --> S{0} ({1}, didn't changed)".format(current_state, signal))
            current_state += 0
    else:
        print("S{0} --> S{0} ({1}, didn't changed)".format(current_state, signal))
        current_state += 0
    return current_state

start = 0
state = start
for signal in signals:
    state = move(state, signal)


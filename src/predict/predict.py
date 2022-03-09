

global counter
counter = 0


def inference(frame):
    print("Running inference...")
    global counter
    counter = counter + 1
    return f"Hey Ho {counter}"

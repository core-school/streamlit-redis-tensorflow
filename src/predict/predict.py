# Count how many predictions we have done
global counter
counter = 0


def inference(frame):
    """
    TODO: Predict with tensorflow or other....
    """
    print("Running inference...")
    global counter
    counter = counter + 1
    return f"Hey Ho {counter}"

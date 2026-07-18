def complex_loop_test():
    total = 0
    # This loop will force the tracer to record hundreds of rapid state changes
    for i in range(100):
        multiplier = i * 1.5
        total += multiplier
    return total

if __name__ == "__main__":
    print("Running stress test...")
    result = complex_loop_test()
    print(f"Done. Final result: {result}")

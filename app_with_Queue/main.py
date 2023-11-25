from console.console_interface import ConsoleInterface

if __name__ == "__main__":
    try:
        console = ConsoleInterface()
        console.run()
    except KeyboardInterrupt:
        pass
    except RuntimeError:
        pass

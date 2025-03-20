import sys


def main():
    getswitchinterval = sys.getswitchinterval
    #setswitchinterval = sys.setswitchinterval
    print("getswitchinterval:", getswitchinterval())
    #print("setswitchinterval:", setswitchinterval)


if __name__ == '__main__':
    main()
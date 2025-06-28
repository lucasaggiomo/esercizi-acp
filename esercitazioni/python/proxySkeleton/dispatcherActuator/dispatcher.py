import sys
from dispatcherImpl import DispatcherImpl
from dispatcherSkel import DispatcherSkel

if __name__ == "__main__":

    try:
        ADDRESS = sys.argv[1]
        PORT = int(sys.argv[2])
    except:
        print("Argomenti non validi o non inseriti")
        sys.exit(1)

    print("Dispatcher Server running...")

    impl = DispatcherImpl()
    skel = DispatcherSkel(ADDRESS, PORT, impl)
    skel.runSkeleton()
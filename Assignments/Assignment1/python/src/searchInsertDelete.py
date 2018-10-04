from readerWriter import LightSwitch
from utils import Semaphore

insertMutex = Semaphore(1)
noSearcher = Semaphore(1)
noInserter = Semaphore(1)
searchSwitch = LightSwitch()
insertSwitch = LightSwitch()


# Search
searchSwitch.wait(noSearcher)
# Critical Section
searchSwitch.signal(noSearcher)

# Insert
insertSwitch.wait(noInserter)
insertMutex.wait()
# Critical Section
insertMutex.signal()
insertSwitch.signal(noInserter)


# Delete
noSearcher.wait()
noInserter.wait()
# Critical Section
noInserter.signal()
noSearcher.signal()
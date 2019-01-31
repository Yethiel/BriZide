"""
Loads BGE Libraries sequentially so that dependencies are met.
"""
import os
from modules import global_constants as G
from bge import logic
from time import sleep
own = logic.getCurrentController().owner

extension = G.EXTENSION_COMPONENT

class Components:

    def __init__(self):
        self.init_loading = False
        self.queue = []
        self.loaded = [None]
        self.opened = [None]
        self.currently_loading = None
        self.currently_loading_str = ""
        self.count = 0

    def enqueue(self, components):
        """Queue components to load them in order"""

        if isinstance(components, str):
            self.queue.append(str(component))

        elif isinstance(components, list):
            for component in components:
                self.queue.append(str(component))


    def load(self):
        """Load the libraries one after another
        All libraries are loaded in a separate thread. Only one lib is loaded
        at a time.
        Run each tick!
        """

        if not self.init_loading and self.queue:
            self.init_loading = True
            self.count = len(self.queue)


        if self.queue:
            # if G.DEBUG: sleep(0.2)
            if not self.currently_loading:
                print(own.name, "Loading",self.queue[0])

                # Make a path from the component name
                blend_path = logic.expandPath("{}{}{}".format(
                    "//components/", self.queue[0], extension))

                # Store the returned status object.
                self.currently_loading = logic.LibLoad(blend_path, "Scene")
                self.currently_loading_str = self.currently_loading.libraryName

                # Add "opened" component to the list, remove it from the queue
                self.opened.append(self.queue[0])
                self.queue.pop(0)

            #Proceed with the next module when the library loaded and the
            #component added itself to the "done" list.
            elif self.currently_loading.finished and self.opened[-1] == self.loaded[-1]:
                print(own.name, "Done loading", self.opened[-1])
                self.currently_loading = None

        else:
            self.init_loading = False
            self.count = 0


    def load_immediate(self, component):
        """Load a library immediately, blocking everything else"""

        if G.DEBUG: print("Loading immediate:", component)

        # blend_path = logic.expandPath("{}{}{}".format(
            # "//components/", component, extension))
        blend_path = os.path.join("{}{}".format(component, extension))

        logic.LibLoad(blend_path, "Scene")

        # self.loaded.append(component)

    def free(self, component):
        """Frees a component that resembles the string. Very loose."""
        for lib in logic.LibList():
            if "{}.blend".format(component) in lib:
                logic.LibFree(lib)  # crashes happen here (randomly and when exiting)
                if G.DEBUG:
                    print("Freed", component)

    def is_done(self, required_components):
        """Takes a list and checks if all modules are loaded"""

        done = True
        for x in required_components:
            if not x in self.loaded:
                done = False
        return done

    def is_loading(self):
        """Returns a boolean whether or not a component is currently loading"""
        return self.init_loading

    def mark_loaded(self, componentstr):
        """Adds a component (string) to the loaded component list"""
        if not componentstr in self.loaded:
            self.loaded.append(componentstr)
            return True
        else:
            return False

    def get_percent(self):
        """Returns the percentage of the components loaded (0<=x<=1)"""
        if self.init_loading:
            return (len(self.loaded) / self.count)
        else:
            return 0

    def get_currently_loading(self):
        """Returns string name of the currently loading component"""
        return self.currently_loading_str

    def clear(self):
        self.init_loading = False
        self.queue = []
        self.loaded = [None]
        self.opened = [None]
        self.currently_loading = None
        self.currently_loading_str = ""
        self.count = 0
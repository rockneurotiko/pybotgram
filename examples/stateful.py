class StatefulTest:
    stateful = False

    def run(self, msg, matches):
        print("state", self.stateful)
        text = "My internal state is: {}".format(self.stateful)
        self.stateful = not self.stateful
        return text


_MyClass = StatefulTest()

__info__ = {
    "description": "Just an example with a class",
    "usage": ["!testclass"],
    "patterns": ["^!testclass$"],
    "run": _MyClass.run
}

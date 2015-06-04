from gl import utils
from PIL import Image
import os


class __ImgToSticker:
    def __init__(self):
        self.users = set()

    def remove_path(self, success, other, npath):
        try:
            os.remove(npath)
        except:
            pass

    def callback(self, success, path, receiver, userid):
        if userid in self.users:
            self.users.remove(userid)
        if success:
            # check if it's an image
            name = path.split("/")[-1].split(".")[0]
            extens = path.split("/")[-1].split(".")[-1]
            if extens.lower() not in ["png", "jpg", "jpeg", "gif"]:
                self.remove_path(True, True, path)
                receiver.send_msg("Sorry, that wasn't an accepted document. I accept png, jpg and gif.")
                return
            npath = "./{}.webp".format(name)
            try:
                im = Image.open(path).convert("RGBA")
                im.save(npath, "WEBP")
                receiver.send_document(npath, utils.gac(self.remove_path, npath))
            except:
                os.remove(npath)
            finally:
                os.remove(path)

    def run(self, msg, matches):
        receiver = utils.get_receiver(msg)
        pattern = matches[0]
        userid = msg.src.id
        if pattern == "photo" or pattern == "document":
            if userid in self.users:
                # Check if he is in the list
                cb = utils.gac(self.callback, receiver, userid)
                getattr(msg, "load_{}".format(pattern))(cb)
        if pattern == "start":
            self.users.add(userid)
            return "You can send me an image now :)"
        if pattern == "stop":
            if userid in self.users:
                self.users.remove(userid)

    def preproc(self, msg):
        # Here maybe deactivate the user if he sends a message and he is activated
        # but this can be a really huge cpu time
        return msg


__MyClass = __ImgToSticker()

__info__ = {
    "description": "Convert a photo to sticker!",
    "usage": ["!imgtosticker start: Next photo you send, as image or document, it will try to convert to sticker and send you.",
              "!imgtosticker stop: Stop the service, won't convert the next image.",
              "If you are in \"start\" mode, send a photo as document or image, and get the sticker!"],
    "patterns": ["^!imgtosticker (start)$",
                 "^!imgtosticker (stop)$",
                 "^\[(photo)\]",
                 "^\[(document)\]"],
    "run": __MyClass.run,
    # "pre_process": __MyClass.preproc
}

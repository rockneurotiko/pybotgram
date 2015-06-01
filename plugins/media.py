import mimetypes
import tgl
from gl import utils


def async_callback_download(path, ext, receiver):
    if path is None:
        return
    mimetype, _ = mimetypes.guess_type(path)
    if not mimetype:
        return
    mime = mimetype.split('/')[0]
    f = tgl.send_file
    if ext == "gif" or ext == "webp" or mime == "text":
        f = tgl.send_document
    elif mime == "image":
        f = tgl.send_image
    elif mime == "audio":
        f = tgl.send_audio
    elif mime == "video":
        f = tgl.send_video
        print("Sending file with mime {} from path {}".format(mimetype, path))
    f(receiver, path, utils.cb_rmp(path))


def synchronous(url, ext, receiver):
    path = ''
    try:
        path = utils.download_to_file(url, ext)
    except:
        print("Error downloading {}".format(url))
        return
    mimetype, _ = mimetypes.guess_type(path)
    if not mimetype:
        return
    mime = mimetype.split('/')[0]
    receiver = utils.get_receiver(msg)
    f = tgl.send_file
    if ext == "gif" or ext == "webp" or mime == "text":
        f = tgl.send_document
    elif mime == "image":
        f = tgl.send_image
    elif mime == "audio":
        f = tgl.send_audio
    elif mime == "video":
        f = tgl.send_video
    print("Sending file with mime {} from path {}".format(mimetype, path))
    f(receiver, path, utils.cb_rmp(path))


__info__ = {
    "description": "When user sends media URL (ends with gif, mp4, pdf, etc.) download and send it to origin.",
    "usage": ["This plugin is automatic when you send an URL."],
    "patterns": [
        "(https?://[\w\-\_\.\?\:\/\+\=\&]+\.(gifv|gif|mp4|pdf|ogg|zip|mp3|rar|wmv|doc|avi|webp))",
    ],
    "run": run,
}

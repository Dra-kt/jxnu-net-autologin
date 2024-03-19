try:
    import winotify
except ImportError:
    pass


def send_notification(title, message):
    if 'winotify' not in globals():
        return
    note = winotify.Notification(title=title, app_id="jxnu-net-autologin", msg=message)
    note.show()

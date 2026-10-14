import base64
import re

LOGO = (
    '<svg viewBox="0 0 200 200" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="r" x1="0%" y1="0%" '
    'x2="100%" y2="100%">'
    '<stop offset="0%" stop-color="#ff69b4"/>'
    '<stop offset="50%" stop-color="#c026d3"/>'
    '<stop offset="100%" stop-color="#a855f7"/>'
    '</linearGradient>'
    '<radialGradient id="s" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%" stop-color="#fffbe6"/>'
    '<stop offset="50%" stop-color="#ffd966"/>'
    '<stop offset="100%" stop-color="#b8860b"/>'
    '</radialGradient></defs>'
    '<circle cx="100" cy="100" r="78" fill="none" '
    'stroke="url(#r)" stroke-width="9"/>'
    '<path d="M100,45 Q108,88 155,100 Q108,112 '
    '100,155 Q92,112 45,100 Q92,88 100,45 Z" '
    'fill="url(#s)" stroke="#d4a017"/>'
    '</svg>'
)

ROSE = (
    '<svg viewBox="0 0 100 100" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<defs><radialGradient id="rp1" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%" stop-color="#ffb6d5"/>'
    '<stop offset="60%" stop-color="#ff69b4"/>'
    '<stop offset="100%" stop-color="#c71585"/>'
    '</radialGradient></defs>'
    '<ellipse cx="50" cy="50" rx="42" ry="38" '
    'fill="url(#rp1)" opacity="0.9"/>'
    '</svg>'
)

LOGO_URI = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(LOGO.encode("utf-8")).decode("utf-8")
)
ROSE_URI = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(ROSE.encode("utf-8")).decode("utf-8")
)


def md(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t.replace("\n", "<br>")

# END

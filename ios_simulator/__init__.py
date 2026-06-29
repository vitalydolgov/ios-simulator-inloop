"""iOS UI automation extension powered by Appium."""

from inloop import contrib

from ios_simulator import wrappers
from ios_simulator.driver import driver


@contrib.tool(
    name="connect",
    description=(
        "Starts a new Appium session, installing WebDriverAgentRunner on the device if needed. "
        "Use when the session is missing, the app was reinstalled, or the device was rebooted. "
        "Does not take any arguments; returns 'ok' on success."
    ),
    parameters={"type": "object", "properties": {}},
)
def connect(args: dict[str, object]) -> None:
    driver.connect()


@contrib.tool(
    name="launch_app",
    description=(
        "Launches an iOS app by bundle ID on the connected device or simulator. "
        "Use at the start of a session or after the app has been closed. "
        "Returns an error if the session is not active or the bundle ID is invalid."
    ),
    parameters={
        "type": "object",
        "properties": {
            "bundle_id": {
                "type": "string",
                "description": "The app's bundle ID, e.g. 'com.example.AppiumDemo'.",
            },
        },
        "required": ["bundle_id"],
    },
)
def launch_app(args: dict[str, object]) -> None:
    wrappers.launch_app(str(args["bundle_id"]))


@contrib.tool(
    name="click",
    description=(
        "Taps a UI element found by its accessibility identifier. "
        "Use to trigger buttons, links, or any tappable element in the running iOS app. "
        "Returns an error if no element with that identifier is found."
    ),
    parameters={
        "type": "object",
        "properties": {
            "identifier": {
                "type": "string",
                "description": "The accessibility identifier of the element to tap.",
            },
        },
        "required": ["identifier"],
    },
)
def click(args: dict[str, object]) -> None:
    wrappers.click(str(args["identifier"]))


@contrib.tool(
    name="type_into_alert",
    description=(
        "Types text into the text field inside an alert dialog. "
        "Use when an alert with a text input is shown and the field has no accessibility identifier. "
        "Fails if no text field is found; use type_into when an accessibility identifier is available."
    ),
    parameters={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text to type.",
            },
        },
        "required": ["text"],
    },
)
def type_into_alert(args: dict[str, object]) -> None:
    wrappers.type_into_alert(str(args["text"]))


@contrib.tool(
    name="type_into",
    description=(
        "Types text into an element found by its accessibility identifier. "
        "Use to fill text fields, search bars, or any focusable input in the running iOS app. "
        "Does not clear existing text first; use before or after clearing if needed."
    ),
    parameters={
        "type": "object",
        "properties": {
            "identifier": {
                "type": "string",
                "description": "The accessibility identifier of the input element.",
            },
            "text": {
                "type": "string",
                "description": "The text to type.",
            },
        },
        "required": ["identifier", "text"],
    },
)
def type_into(args: dict[str, object]) -> None:
    wrappers.type_into(str(args["identifier"]), str(args["text"]))


@contrib.tool(
    name="inspect",
    description=(
        "Returns the full accessibility tree of the current screen as JSON. "
        "Use to discover element identifiers, types, and hierarchy when you don't know what's on screen. "
        "Output can be large; prefer find_element or find_element_by_type when the identifier is already known."
    ),
    parameters={"type": "object", "properties": {}},
)
def inspect(args: dict[str, object]) -> str:
    return wrappers.inspect()


@contrib.tool(
    name="find_element_by_type",
    description=(
        "Finds an element by its XCUIElement type and optional name, returning its attributes as JSON. "
        "Use when the element has no accessibility identifier but its type (button, text_field) and name are known. "
        "Omit name to match the first element of that type; use find_element when an accessibility identifier is available."
    ),
    parameters={
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["button", "text_field"],
                "description": "The XCUIElement type.",
            },
            "name": {
                "type": "string",
                "description": "The element name as it appears in the UI, e.g. 'Add'.",
            },
        },
        "required": ["type"],
    },
)
def find_element_by_type(args: dict[str, object]) -> str:
    name = str(args["name"]) if "name" in args else None
    return wrappers.find_element_by_type(str(args["type"]), name)


@contrib.tool(
    name="swipe",
    description=(
        "Swipes a table cell left or right by its visible text label using a drag gesture. "
        "Use to trigger swipe actions like revealing delete or action buttons on a row. "
        "Does not scroll the screen; operates only on the matched cell."
    ),
    parameters={
        "type": "object",
        "properties": {
            "label": {
                "type": "string",
                "description": "The visible text label of the cell to swipe, e.g. 'Buy milk'.",
            },
            "direction": {
                "type": "string",
                "enum": ["left", "right"],
                "description": "The swipe direction.",
            },
        },
        "required": ["label", "direction"],
    },
)
def swipe(args: dict[str, object]) -> None:
    wrappers.swipe(str(args["label"]), str(args["direction"]))


@contrib.tool(
    name="find_element",
    description=(
        "Finds a single iOS UI element by accessibility identifier and returns its identifier, text, enabled, displayed, location, and size as JSON. "
        "Use when inspecting or asserting properties of a specific element in the running iOS app. "
        "Requires the accessibility identifier to already be known; use inspect to discover it or find_element_by_type when only the element type and name are known."
    ),
    parameters={
        "type": "object",
        "properties": {
            "identifier": {
                "type": "string",
                "description": "The accessibility identifier of the element.",
            },
        },
        "required": ["identifier"],
    },
)
def find_element(args: dict[str, object]) -> str:
    return wrappers.find_element(str(args["identifier"]))


EXTENSION = contrib.Extension(
    name="ios_simulator",
    tools=[
        connect,
        launch_app,
        click,
        swipe,
        type_into_alert,
        type_into,
        inspect,
        find_element_by_type,
        find_element,
    ],
)

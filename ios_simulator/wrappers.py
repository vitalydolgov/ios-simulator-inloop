"""Appium iOS wrappers."""

import json
import time

import xmltodict

from appium.webdriver.common.appiumby import AppiumBy

from ios_simulator.driver import driver


_XCUI_TYPES = {
    "button": "XCUIElementTypeButton",
    "text_field": "XCUIElementTypeTextField",
    "static_text": "XCUIElementTypeStaticText",
}


def inspect() -> str:
    """Return the accessibility tree of the current screen as JSON."""
    return json.dumps(xmltodict.parse(driver.session.page_source))


def launch_app(bundle_id: str) -> None:
    """Launch the app with the given bundle ID."""
    driver.session.activate_app(bundle_id)


def click(identifier: str) -> None:
    """Tap the element with the given accessibility identifier."""
    driver.session.find_element(AppiumBy.ACCESSIBILITY_ID, identifier).click()


def swipe(label: str, direction: str) -> None:
    """Swipe a cell left or right by its static text label."""
    element = driver.session.find_element(AppiumBy.XPATH, f"//XCUIElementTypeCell[.//XCUIElementTypeStaticText[@label='{label}']]")
    loc = element.location
    size = element.size
    mid_y = loc["y"] + size["height"] / 2
    half_width = size["width"] * 0.5

    if direction == "right":
        from_x = loc["x"] + 20
        to_x = from_x + half_width
    else:
        from_x = loc["x"] + size["width"] - 20
        to_x = from_x - half_width

    driver.session.execute_script("mobile: dragFromToForDuration", {
        "fromX": from_x, "fromY": mid_y,
        "toX": to_x, "toY": mid_y,
        "duration": 1.0,
    })
    time.sleep(0.5)


def _element_json(element) -> str:
    name = element.get_attribute("name")
    return json.dumps({
        "identifier": name.split(":", 1)[-1] if name else None,
        "text": element.text,
        "enabled": element.is_enabled(),
        "displayed": element.is_displayed(),
        "location": element.location,
        "size": element.size,
    })


def type_into_alert(text: str) -> None:
    """Type text into the text field inside an alert dialog."""
    driver.session.find_element(AppiumBy.XPATH, f"//{_XCUI_TYPES['text_field']}").send_keys(text)


def type_into(identifier: str, text: str) -> None:
    """Type text into an element with the given accessibility identifier."""
    driver.session.find_element(AppiumBy.ACCESSIBILITY_ID, identifier).send_keys(text)


def find_element(identifier: str) -> str:
    """Locate a single iOS UI element and return its attributes."""
    element = driver.session.find_element(AppiumBy.ACCESSIBILITY_ID, identifier)
    return _element_json(element)


def find_element_by_type(type: str, name: str | None = None) -> str:
    """Find an element by its XCUIElement type and optional name."""
    xcui_type = _XCUI_TYPES.get(type)
    if xcui_type is None:
        raise ValueError(f"unsupported type '{type}', supported: {list(_XCUI_TYPES)}")
    selector = f"//{xcui_type}[@name='{name}']" if name else f"//{xcui_type}"
    element = driver.session.find_element(AppiumBy.XPATH, selector)
    return _element_json(element)

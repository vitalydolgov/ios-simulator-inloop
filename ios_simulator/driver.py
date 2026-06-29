"""Appium driver singleton for iOS."""

import os

from appium import webdriver
from appium.options.ios import XCUITestOptions


class Driver:
    """Manages a single Appium session, reconnecting on demand."""

    def __init__(self):
        self._session = None

    @property
    def session(self) -> webdriver.Remote:
        """Return the active session, opening one if needed."""
        if self._session is None:
            self._session = self._open()
        return self._session

    def connect(self) -> None:
        """Quit any active session and open a fresh one."""
        if self._session is not None:
            try:
                self._session.quit()
            except Exception:
                pass
            self._session = None
        self.session

    def _open(self) -> webdriver.Remote:
        options = XCUITestOptions()

        bundle_id = os.environ.get("APPIUM_BUNDLE_ID", "")
        if bundle_id:
            options.bundle_id = bundle_id

        udid = os.environ.get("APPIUM_UDID", "")
        if udid:
            options.udid = udid

        platform_version = os.environ.get("APPIUM_PLATFORM_VERSION", "")
        if platform_version:
            options.platform_version = platform_version

        url = os.environ.get("APPIUM_URL", "http://127.0.0.1:4723")
        return webdriver.Remote(url, options=options)


driver = Driver()

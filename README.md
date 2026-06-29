# iOS Simulator Control (Inloop extension)

iOS UI automation extension for [Inloop](https://github.com/vitalydolgov/inloop), powered by Appium.

## Prerequisites

### Appium

Install Appium and the XCUITest driver:

```sh
npm install -g appium
appium driver install xcuitest
```

Optionally verify your environment with `appium-doctor`:

```sh
npm install -g @appium/doctor
appium-doctor --ios
```

Start the Appium server:

```sh
appium
```

### Simulator

List, boot, and open a simulator:

```sh
xcrun simctl list devices
xcrun simctl boot "<device-name>"
open -a Simulator
```

## Install into Inloop

Clone the Inloop framework and follow its setup procedure:

```sh
git clone https://github.com/vitalydolgov/inloop
cd inloop
```

Setup steps are in the [Inloop README](https://github.com/vitalydolgov/inloop#readme). Then install this extension from a path or git url:

```sh
# by path
uv run extensions install ../ios-simulator-inloop

# by git url (optionally pin a branch/tag/commit)
uv run extensions install "git+https://github.com/vitalydolgov/ios-simulator-inloop"
```

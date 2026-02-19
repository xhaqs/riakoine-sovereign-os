[app]
title = Riakoine Sentinel
package.name = riakoine_os
package.domain = empire.riakoine
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,yml
version = 0.1
requirements = python3,kivy
orientation = portrait
android.permissions = INTERNET,VIBRATE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

title = SEPA Transfer Manager
package.name = sepatransfer
package.domain = org.sepatransfer

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0
requirements = python3,kivy,requests,sqlalchemy,pydantic

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

android.features = android.hardware.internet

p4a.url = https://github.com/kivy/python-for-android/archive/develop.zip
p4a.branch = develop
p4a.private_storage_dir = .buildozer/android/platform/build-{arch}/other_builds

android.arch = armeabi-v7a

log_level = 2
warn_on_root = 1
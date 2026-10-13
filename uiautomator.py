
import uiautomator2 as u2

d = u2.connect("AWCX6R3C15018090")

# បើឃើញ Popup ដែលមានពាក្យ Allow នោះចុច Allow
d.watcher.when(text="Allow").click()

# ចាប់ផ្ដើមត្រួតពិនិត្យ Popup
d.watcher.start()

# ធ្វើសកម្មភាពផ្សេងៗតាមតម្រូវការ
d.app_start("com.facebook.katana")

# បញ្ឈប់ Watcher នៅពេលមិនត្រូវការទៀត
d.watcher.stop()

d.clear_text()
d.press("back")
d.press("home")
d.press("enter")

# អូសពីខាងក្រោមទៅខាងលើ ដើម្បី Scroll ចុះមើលមាតិកាបន្ថែម
d.swipe(500, 900, 500, 300, duration=0.5)

# អូសពីឆ្វេងទៅស្តាំ
d.swipe(100, 500, 800, 500, duration=0.5)

# អូសពីចំណុចចាប់ផ្ដើមទៅចំណុចបញ្ចប់
d.drag(200, 400, 700, 400, duration=1)

# អូសឡើងដោយប្រើទិសដៅ
d.swipe_ext("up", scale=0.8)

# អូសចុះ
d.swipe_ext("down", scale=0.8)

# អូសទៅឆ្វេង
d.swipe_ext("left")

# អូសទៅស្តាំ
d.swipe_ext("right")
# ចុច Element ដែលមានអត្ថបទ Next
d(text="Next").click()

# ចុចទីតាំង x=500, y=300
d.click(500, 300)

# ចុចពីរដងនៅទីតាំងកំណត់
d.double_click(500, 300)

# ចុចសង្កត់រយៈពេល 1 វិនាទី
d.long_click(500, 300, duration=1)

# វាយអត្ថបទទៅក្នុងប្រអប់ដែលបាន Focus
d.send_keys("Hello World")

# លុបអត្ថបទចាស់ រួចវាយអត្ថបទថ្មី
d.send_keys("New Text", clear=True)

# ជ្រើសប្រអប់ Email មុននឹងវាយអត្ថបទ
d(resourceId="com.example:id/email").click()
d.send_keys("example@gmail.com")

# ចុចប៊ូតុង Enter លើ Android
d.press("enter")

# ចុច Back
d.press("back")

# ចុច Home
d.press("home")

# បើក Recent Apps
d.press("recent")

# បង្កើតសារ Toast បង្ហាញលើអេក្រង់
d.make_toast("បានបញ្ចប់", duration=2)
# ថតរូបអេក្រង់ ហើយរក្សាទុកជាឯកសារ PNG
d.screenshot("screen.png")

# ថតរូបហើយទទួលបានរូបភាពសម្រាប់ប្រើក្នុង Python
image = d.screenshot()

# បង្វិលអេក្រង់ទៅទម្រង់ផ្ដេក
d.set_orientation("l")

# បង្វិលអេក្រង់ទៅទម្រង់បញ្ឈរ
d.set_orientation("n")

# ចាក់សោការបង្វិលអេក្រង់
d.freeze_rotation()

# អនុញ្ញាតឱ្យអេក្រង់បង្វិលវិញ
d.freeze_rotation(False)

# បើកផ្ទាំង Notification
d.open_notification()

# បើកផ្ទាំង Quick Settings
d.open_quick_settings()

# បង្ហាញសញ្ញាប៉ះលើអេក្រង់
d.show_touch_trace()

# បិទសញ្ញាប៉ះលើអេក្រង់
d.show_touch_trace(pointer_location=False, show_touches=False)
# ពិនិត្យ Android Version តាម Shell
result = d.shell("getprop ro.build.version.release")
print(result.output)

# ពិនិត្យ Device Model
result = d.shell("getprop ro.product.model")
print(result.output)

# បង្ហាញ IP របស់ Wi-Fi
print(d.wlan_ip)

# បង្ហាញ Serial Number របស់ Device
print(d.serial)

# បើកកម្មវិធី Settings
d.shell("am start -a android.settings.SETTINGS")

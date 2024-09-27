from core.file_paths import *


def is_new_component(line: str):
    if f"E: " in line:
        return True
    return False


def transform_activtiy_name(activity_name: str, package_name: str):
    activity_name = activity_name.strip()
    if f"{package_name}." in activity_name:
        activity_name = activity_name.replace(f"{package_name}.", f"{package_name}/.")
    else:
        activity_name = f"{package_name}/{activity_name}"
    return activity_name


def parse_manifest_file(apk_path: str):
    activities = set()
    permissions = set()
    exported_activities = set()
    cmd = f"aapt dump xmltree {apk_path} AndroidManifest.xml"
    lines = os.popen(cmd).read().split("\n")
    is_activity = False
    is_permission = False
    is_exported = False
    package_name = ""
    name = ""
    for line in lines:
        try:
            if "A: package=" in line:
                package_name = line.split('\"')[1]
            if is_new_component(line):
                if name != "":
                    if is_activity:
                        activity = name
                        activities.add(activity)
                        if is_exported:
                            exported_activities.add(activity)
                    if is_permission:
                        permission = name
                        permissions.add(permission)
                is_activity = False
                is_permission = False
                is_exported = False
                name = ""
            if "E: activity" in line:
                is_activity = True
            if "E: uses-permission" in line:
                is_permission = True
            if "A: android:name" in line:
                name = line.split('=\"')[1].split('\" (Raw:')[0]
            if "A: android:exported" in line and "0xffffffff" in line:
                is_exported = True
        except:
            print(f"Error while parse line: {line}")
    result_activities = set()
    for activity in activities:
        result_activities.add(transform_activtiy_name(activity, package_name))
    result_activities = list(result_activities)
    return package_name, permissions, result_activities, exported_activities


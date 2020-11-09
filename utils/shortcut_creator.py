from win32com.client import Dispatch
import os
import re


class shortcut:
    def __init__(self):
        self.root_dir = os.getcwd()
        self.shortcut_dir = self.root_dir + "/shortcuts"

        self.appdata = os.getenv("APPDATA")
        self.dir_zoom = self.appdata + "/Zoom/bin"
        self.exe_zoom = self.dir_zoom + "/Zoom.exe"

        # Make /shortcut directory
        try:
            os.mkdir(self.shortcut_dir)
        except(FileExistsError):
            pass

    # Remove spaces in meetingID
    def meeting_convert(self, ID):
        split = re.split(r"\s+", ID)
        newMeetingID = split[0] + split[1] + split[2]
        return(newMeetingID)

    # Create shortcut
    def create_shortcuts(self, identifier, exe_path, startin, icon_path, args, directory):
        shell = Dispatch('WScript.Shell')
        shortcut_file = os.path.join(directory, identifier + '.lnk')
        shortcut = shell.CreateShortCut(shortcut_file)
        shortcut.Targetpath = exe_path
        shortcut.Arguments = args
        shortcut.WorkingDirectory = startin
        shortcut.IconLocation = icon_path
        shortcut.save()
        print("Shortcut for [ {} ] created...".format(identifier))

    def create(self, identifier, meetingID):
        try:
            newID = self.meeting_convert(meetingID)
            TARGET = '"--url=zoommtg://zoom.us/join?action=join&confno={}"'.format(str(newID))
            print("*** CREATING SHORTCUT ***")

            self.create_shortcuts(identifier, self.exe_zoom, self.dir_zoom, self.exe_zoom, TARGET, self.shortcut_dir)
            return(True)
        except(TypeError):
            print("ERROR: [TypeError]")
            return(False)

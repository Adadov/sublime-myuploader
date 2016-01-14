import sublime, sublime_plugin
import re, os
import pprint
import subprocess

class MyuploaderBkpfile(sublime_plugin.WindowCommand):
    def run(self):
        self.debug = os.getenv("SUBDEBUG", False)

        view = self.window.active_view()
        fullname = view.file_name()

        proc = subprocess.Popen(['cp', fullname, fullname+".bkp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()


class MyuploaderToggledebug(sublime_plugin.WindowCommand):
    def run(self):
        if not os.environ["SUBDEBUG"]:
            print("Debug activé")
            os.environ["SUBDEBUG"] = "True"
            return

        if os.environ["SUBDEBUG"] == "True":
            print("Debug désactivé")
            os.environ["SUBDEBUG"] = "False"
        else:
            print("Debug activé")
            os.environ["SUBDEBUG"] = "True"

class MyuploaderSendCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.debug = os.getenv("SUBDEBUG", False)

        view = self.window.active_view()
        fullname = view.file_name()

        filename = os.path.basename(view.file_name())
        projectLocalPath = view.settings().get("projectLocalPath")
        serverName = view.settings().get("serverName")

        filteredFiles = view.settings().get('filteredFiles', '\\.sublime-[a-z]+$')
        if re.search(filteredFiles, view.file_name()):
            self.printError("L'extension est filtrée")
            return

        if not projectLocalPath:
            self.printError("Le chemin local du projet n'est pas défini ! (projectLocalPath)")
            return

        if not serverName:
            self.printError("Le nom du serveur n'est pas défini ! (serverName)")
            return

        projectSrvPath = view.settings().get("projectSrvPath")

        self.printDebug("Fullname: "+fullname)

        if projectSrvPath: # Destination commune pour tous les fichiers
            self.printDebug("Chemin commun pour tous les fichiers")
            destination = re.sub(projectLocalPath, projectSrvPath, fullname)
        else: # Chaque fichier doit avoir une destination
            self.printDebug("Chemin spécifique pour chaque fichier")
            destinations = view.settings().get("destinations")
            self.printDebug(destinations[filename])
            destination = destinations[filename]

        self.printDebug ("Destination: "+destination)

        print("Sending file", filename, "to", serverName+":"+destination, "...")

        if not destination:
            self.printError("Destination non définie !")
            return

#        ret = view.window().run_command('exec', {"cmd": ["/usr/bin/scp", filename, serverName+":"+destination]})
#        print(ret)
        proc = subprocess.Popen(['scp', filename, serverName+":"+destination], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        print ('result: %s' % repr(proc.stderr.readline()))

    def printDebug(self, msg):
        if self.debug == "True":
            print("[DEBUG] ", msg)

    def printError(self, msg):
        print("[ERREUR] ", msg)

class MyuploaderDebug(sublime_plugin.WindowCommand):
    def printDebug(self, msg):
        if self.debug == "True":
            print("[DEBUG] ", msg)

    def printError(self, msg):
        print("[ERREUR] ", msg)


import subprocess
import shlex
import sublime, sublime_plugin


class TagCommand(sublime_plugin.TextCommand):
    def on_change(self, s):
        pass

    def on_done(self, new_tags):
        # clear old tags
        subprocess.Popen(
            ['openmeta', '-s', '-p', self.filename],
        )
        # set new tags
        tagging_command = ['openmeta', '-a']
        # workaround for strange behaviour in shlex
        tagging_command += [s.decode('utf-8') for s in shlex.split(new_tags.encode('utf-8'))]
        tagging_command += ['-p', self.filename]
        print tagging_command
        subprocess.Popen(
             tagging_command
        )

    def on_cancel(self):
        pass

    def run(self, edit):
        self.window = self.view.window()
        self.filename = self.view.file_name()

        # retrieving tags from file
        output = subprocess.Popen(
            ['openmeta', '-p', self.filename],
            stdout=subprocess.PIPE
        ).communicate()[0]

        lines = output.split('\n')
        tags_prefix_len = 6  # tags: tag1 tag2...
        tags = lines[1][tags_prefix_len:]

        # setting up input panel
        self.window.show_input_panel(
            "Tags:",
            tags + (" " if tags else ""),
            self.on_done, self.on_change, self.on_cancel
            )

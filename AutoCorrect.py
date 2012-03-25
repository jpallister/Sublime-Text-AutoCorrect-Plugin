#import sublime
import sublime_plugin
import SubList
import sublime

corrections = {"bitwdith": "bit-width", "wdith": "width"}


class AutoCorrectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        #self.view.insert(edit, 0, "Hello, World!")
        #self.view.run_command("right_delete")

        rs = self.view.sel()

        for r in rs:
            if r.b - r.a == 0:
                word = self.view.word(r)
                sword = self.view.substr(word)
                can_local_correct = sword in corrections
                correct = SubList.match(sword)
                if max(word.a, word.b) <= r.a and (can_local_correct or correct != ""):
                    print "Correction"

                    if can_local_correct:
                        correct = corrections[sword]
                    sublime.status_message("AutoCorrect: \"" + sword + "\" corrected to \"" + correct + "\"")
                    self.view.replace(edit, word, correct)

            self.view.run_command("insert", {"characters": " "})


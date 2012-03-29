#import sublime
import sublime_plugin
import SubList
import sublime

# Eventually this should be end user updatable
corrections = {"bitwdith": "bit-width", "wdith": "width"}


class AutoCorrectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.end_edit(edit)
        edit = self.view.begin_edit()
        rs = self.view.sel()

        regions_to_correct = []

        for r in rs:
            if r.b - r.a == 0:
                word = self.view.word(r)
                sword = self.view.substr(word)

                can_local_correct = sword in corrections  # locally set should take priority
                correct = SubList.match(sword)

                if max(word.a, word.b) <= r.a and (can_local_correct or correct != ""):
                    if can_local_correct:
                        correct = corrections[sword]

                    regions_to_correct.append((correct, word))
                    sublime.status_message("AutoCorrect: \"" + sword + "\" corrected to \"" + correct + "\"")

        self.view.run_command("insert", {"characters": " "})

        self.view.end_edit(edit)
        edit = self.view.begin_edit()

        for (correct, word) in regions_to_correct:

            self.view.replace(edit, word, correct)

            self.view.add_regions("correction_outline", [self.view.word(word)], "mark", sublime.DRAW_EMPTY)
            sublime.set_timeout(lambda: self.view.erase_regions("correction_outline"), 500)

        self.view.end_edit(edit)



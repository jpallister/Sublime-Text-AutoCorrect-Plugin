#import sublime
import sublime_plugin
import SubList
import sublime
import functools

# Eventually this should be end user updatable
corrections = {"bitwdith": "bit-width", "wdith": "width"}


class AutoCorrectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.end_edit(edit)
        edit = self.view.begin_edit()
        rs = self.view.sel()

        regions_to_correct = []

        self.view.run_command("insert", {"characters": " "})

        for r in rs:
            if r.b - r.a == 0:
                word = self.view.word(r.begin() - 1)
                sword = self.view.substr(word)

                can_local_correct = sword in corrections  # locally set should take priority
                correct = SubList.match(sword)

                if word.end() <= r.begin() - 1 and (can_local_correct or correct != ""):
                    if can_local_correct:
                        correct = corrections[sword]

                    regions_to_correct.append((correct, word))
                    sublime.status_message("AutoCorrect: \"" + sword + "\" corrected to \"" + correct + "\"")

        self.view.end_edit(edit)
        edit = self.view.begin_edit()

        for i, (correct, word) in enumerate(regions_to_correct[::-1]):
            reg = self.view.word(word)
            self.view.replace(edit, reg, correct)

            self.view.add_regions("correction_outline" + str(i), [self.view.word(reg.begin())], "mark", sublime.DRAW_EMPTY)

        sublime.set_timeout(functools.partial(self.remove_regions, len(regions_to_correct)), 500)

        self.view.end_edit(edit)

    def remove_regions(self, n):
        for i in range(n):
            self.view.erase_regions("correction_outline" + str(i))

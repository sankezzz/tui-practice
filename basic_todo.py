from textual.app import App, ComposeResult
from textual.widgets import Input, ListView, ListItem, Label


class MyApp(App):
    CSS="""
    Screen {
    align: center middle;
}

ListView {
    width: auto;
    height: auto;
    margin: 2 2;
}

Label {
    padding: 1 2;
}
"""

    BINDINGS=[("d","delete","delete a highlighted task"),("e","edit","edits a given todo")] #(key, action_name , here delete and the fucntion name is action_delete so it fires when pressed d , description)

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type a task and press Enter",id="title")
        yield Input(placeholder="Enter the description of todo ",id="desc")
        yield ListView()                       # empty list at startup
        

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:                           # ignore empty Enters
            return
        new_row = ListItem(Label(text))        # build one row
        self.query_one(ListView).append(new_row)   # add it to the screen, live
        #Query one gives the widget data that has been passed  -- we can make focus on that 
        event.input.value = ""

    def action_delete(self)->None:
        row = self.query_one(ListView).highlighted_child ## this the highlighted row when we move around with the arrow keys 
        if row is not None:
            row.remove()




MyApp().run()
from textual.app import App, ComposeResult
from textual.containers import Vertical # this verticle is one of the containeers 

from textual.widgets import Input, ListView, ListItem, Label,Static,RadioSet


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

    def on_mount(self) -> None:
        self.data = {} 
        self.selected_row = None        # remember which todo the detail panel is showing


    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type a task and press Enter",id="title")
        yield Input(placeholder="Enter the description of todo ",id="desc")
        yield ListView()                       # empty list at startup
        yield Vertical(id="detail")     # an EMPTY container we fill on selection


        

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id=="title": # when pressed enter in title focus goes to the descitpion box for input 
            self.query_one("#desc", Input).focus() # we can make the focous come to this place itself 
            return 
        
        # Enter in the desc box -> create the todo
        title = self.query_one("#title", Input).value.strip() #we can use the same for the description but the event has the desc value that we just put 
        desc = event.value.strip()
        if not title:
            return 
        
        row=ListItem(Label(title))
        self.query_one(ListView).append(row)
        self.data[row] = {"title": title, "description": desc}

        #after the row is appended to list item and the list only has the title no desc -- desc only when clicked on the todo 
        self.query_one("#title", Input).value = ""
        self.query_one("#desc", Input).value = ""
        self.query_one("#title", Input).focus() #gets control over to the title directly 

    async def on_list_view_selected(self,event:ListView.Selected)->None:
        #whenever the listview is selected 
        info=self.data[event.item] #lookup in the dict
        # detail = self.query_one("#detail", Static) #find the widget with id = detail we create a new detail widget here to show the widget 
        # detail.update(f"{info['title']}\n\n{info['description']}") # this gives a static title and desc 
        panel = self.query_one("#detail", Vertical)
        await panel.remove_children()               # clear whatever was there
        await panel.mount(Static(info["title"]))    # mount fresh widgets
        await panel.mount(Static(info["description"]))
        await panel.mount(RadioSet("Todo", "Doing", "Done"))   # a totally different widget


    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        # fires when the user picks a radio option
        if self.selected_row is not None:
            self.data[self.selected_row]["status"] = str(event.pressed.label)  # the color changed 

    

    def action_delete(self)->None:
        row = self.query_one(ListView).highlighted_child ## this the highlighted row when we move around with the arrow keys 
        if row is not None:
            self.data.pop(row,None) # here just one thing is added which is popping the row itself from the json then removing from ui 
            row.remove()




MyApp().run()
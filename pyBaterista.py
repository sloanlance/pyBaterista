import ui
import sound

DRUM_SOUNDS = [
  'drums:Drums_01', 'drums:Drums_02', 'drums:Drums_03', 'drums:Drums_04', 
  'drums:Drums_05', 'drums:Drums_06', 'drums:Drums_07', 'drums:Drums_08', 
  'drums:Drums_09', 'drums:Drums_10', 'drums:Drums_11', 'drums:Drums_12', 
  'drums:Drums_13', 'drums:Drums_14', 'drums:Drums_15', 'drums:Drums_16', ]

PADDING = 20
COLUMNS = 8
ROWS = 16

FLASH_COLOR = '#FFFF66'  # Light yellow

MAX_W, MAX_H = ui.get_window_size()

BUTTON_WIDTH = MAX_W // COLUMNS - PADDING
BUTTON_HEIGHT = MAX_H // ROWS - PADDING

@ui.in_background
def play_and_flash(sender):
    sound.play_effect(sender.sound_name)
    print(sender.superview.name)
    # If already flashing, reset color
    if hasattr(sender, 'flash_restore_pending') and sender.flash_restore_pending:
        ui.cancel_delays()  # Will cancel all pending ui.delay calls
        sender.background_color = sender.base_color
        sender.flash_restore_pending = False
    # Start flash
    sender.bg_color = FLASH_COLOR
    sender.flash_restore_pending = True
    # Schedule restore
    def restore():
        sender.bg_color = sender.base_color
        sender.flash_restore_pending = False
    ui.delay(restore, 0.12)

class DrumPad(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = 'black'
        self.flash_color = 'yellow'
        self.name = 'DrumPad main view'
        self.original_bg_color = self.background_color
        self.build_grid()
        
    def present(self, *args, **kwargs):
        # First, call the superclass's present method to show the view as usual
        super().present(*args, **kwargs)
        # Now do your extra tasks.
        print('DrumPad has been presented!')
        # For example, you could start an animation or setup additional features here.    
        
    def build_grid(self):
        for col in range(COLUMNS):
            colView = ui.View(
              background_color = ('blue', 'grey')[col % 2],
              #background_color = 'clear',
              name=f'colView_{col}',
              #alpha=0.5,
              frame = (
                col * (BUTTON_WIDTH + PADDING) + PADDING,
                0,
                BUTTON_WIDTH + PADDING,
                MAX_H
              )
            )
            self.add_subview(colView)
            for row in range(ROWS):
                #idx = row * COLUMNS + col
                idx = row
                base_color = 'orange'
                btn = ui.Button(
                    bg_color=base_color,
                    title=str(idx + 1),
                    border_width=2,
                    border_color='white',
                    corner_radius=10,
                    tint_color='white'
                )
                btn.frame = (
                    PADDING // 2,
                    PADDING + row * (BUTTON_HEIGHT + PADDING),
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT
                )
                
                # Store our extra state directly on the button
                btn.base_color = base_color
                btn.sound_name = DRUM_SOUNDS[idx]
                btn.flash_restore_pending = False
                btn.action = play_and_flash
                colView.add_subview(btn)
            self.add_subview(colView)


if __name__ == '__main__':
    w = (BUTTON_WIDTH + PADDING) * COLUMNS + PADDING
    h = (BUTTON_HEIGHT + PADDING) * ROWS + PADDING
    print(f'{w=}, {h=}')
    view = DrumPad()
    view.frame = (0, 0, w, h)
    print(view.height, view.width)    
    view.present('full_screen', hide_title_bar=True)
    print(view.height, view.width)


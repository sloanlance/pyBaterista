import sound
import time
import ui

DRUM_SOUNDS = [
  'drums:Drums_01', 'drums:Drums_02', 'drums:Drums_03', 'drums:Drums_04',
  'drums:Drums_05', 'drums:Drums_06', 'drums:Drums_07', 'drums:Drums_08',
  'drums:Drums_09', 'drums:Drums_10', 'drums:Drums_11', 'drums:Drums_12',
  'drums:Drums_13', 'drums:Drums_14', 'drums:Drums_15', 'drums:Drums_16', ]

PADDING = 10
COLUMNS = 16
ROWS = 16

FLASH_COLOR = '#FFFFE0'  # Light yellow

MAX_W, MAX_H = ui.get_window_size()

BUTTON_WIDTH = MAX_W // COLUMNS - PADDING
BUTTON_HEIGHT = MAX_H // ROWS - PADDING

@ui.in_background
def play_and_flash1(sender):
    sound.play_effect(sender.sound_name)
    sender.bg_color = FLASH_COLOR
    # Store a timestamp to identify the current flash
    now = time.time()

    def restore():
        # Only restore if no newer flash has happened
        if getattr(sender, '_flash_time', None) == now:
            sender.bg_color = sender.base_color
            sender._flash_time = None

    if getattr(sender, '_flash_time', None) is None:
        sender._flash_time = now
        ui.delay(restore, 0.12)

@ui.in_background
def play_and_flash(sender):
    #print(sender.superview.name)
    sound.play_effect(sender.sound_name)
    sender.bg_color = FLASH_COLOR

    def restore():
        sender.bg_color = sender.base_color

    ui.delay(restore, 0.12)

class DrumPad(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = 'black'
        self.name = 'DrumPad main view'
        self.original_bg_color = self.background_color
        self.column_views = []
        self.previous_highlight = None
        self.highlight_index = 0
        self.build_grid()

    def present(self, *args, **kwargs):
        super().present(*args, **kwargs)
        print('DrumPad has been presented!')
        self.start_column_highlight_loop()

    def build_grid(self):
        for col in range(COLUMNS):
            #col_color = ('blue', 'grey')[col % 2]
            col_color = 'clear'
            colView = ui.View(
              background_color = col_color,
              name=f'colView_{col}',
              #alpha=0.5,
              frame = (
                col * (BUTTON_WIDTH + PADDING) + PADDING,
                0,
                BUTTON_WIDTH + PADDING,
                MAX_H
              )
            )
            colView.original_color = col_color
            self.column_views.append(colView)
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
                btn.base_color = base_color
                btn.sound_name = DRUM_SOUNDS[idx]
                btn.flash_restore_pending = False
                btn.action = play_and_flash
                colView.add_subview(btn)
            self.add_subview(colView)

    def start_column_highlight_loop(self):
        self.highlight_columns_loop()

    def highlight_columns_loop(self):
        # Un-highlight previous
        if self.previous_highlight is not None:
            prev_col = self.column_views[self.previous_highlight]
            prev_col.background_color = prev_col.original_color
        # Highlight current
        current_col = self.column_views[self.highlight_index]
        current_col.background_color = '#cffdbc'  # verypalegreen
        self.previous_highlight = self.highlight_index
        self.highlight_index = (self.highlight_index + 1) % COLUMNS
        ui.delay(self.highlight_columns_loop, 1.0)

if __name__ == '__main__':
    w = (BUTTON_WIDTH + PADDING) * COLUMNS + PADDING
    h = (BUTTON_HEIGHT + PADDING) * ROWS + PADDING
    view = DrumPad()
    view.frame = (0, 0, w, h)
    print(view.height, view.width)
    view.present('full_screen', hide_title_bar=True)
    print(view.height, view.width)


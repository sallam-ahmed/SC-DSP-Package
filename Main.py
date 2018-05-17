from Interfaces.main_window import MainInterface
from Interfaces.main_window_binder import MainInterfaceBinder


if __name__ == "__main__":
    app = MainInterface()
    eventsManager = MainInterfaceBinder(app)
    eventsManager.BindEvents()
    app.mainloop()

from SignalOperator.iMain import MainInterface
from SignalOperator.iMainBinder import MainInterfaceBinder

        
if __name__ == "__main__":        
        app = MainInterface()
        eventsManager = MainInterfaceBinder(app)
        eventsManager.BindEvents()
        app.mainloop()
        